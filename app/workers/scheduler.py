import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import settings
from app.db.database import SessionLocal
from app.services.ai_service import classify
from app.services.export_service import send_result
from app.services.task_service import (
    claim_one_pending,
    list_done_for_export,
    mark_done,
    mark_failed_or_retry,
    mark_sent,
    reset_stuck,
)

logger = logging.getLogger(__name__)


def process_pending() -> None:
    db = SessionLocal()
    try:
        task = claim_one_pending(db)
        if task is None:
            return

        logger.info(
            "Task %s (external_id=%s) claimed, status=processing",
            task.id,
            task.external_id,
        )
        try:
            result = classify(task.input_text)
            mark_done(db, task, result)
            logger.info(
                "Task %s (external_id=%s) status=done, result=%s",
                task.id,
                task.external_id,
                result,
            )
        except Exception as exc:
            mark_failed_or_retry(db, task, str(exc))
            db.refresh(task)
            if task.status == "failed":
                logger.warning(
                    "Task %s (external_id=%s) status=failed after %d attempts: %s",
                    task.id,
                    task.external_id,
                    task.attempts,
                    exc,
                )
            else:
                logger.warning(
                    "Task %s (external_id=%s) status=pending, retry %d/%d: %s",
                    task.id,
                    task.external_id,
                    task.attempts,
                    settings.MAX_ATTEMPTS,
                    exc,
                )
    finally:
        db.close()


def export_done() -> None:
    db = SessionLocal()
    try:
        tasks = list_done_for_export(db)
        for task in tasks:
            try:
                if send_result(task):
                    mark_sent(db, task)
                    logger.info(
                        "Task %s (external_id=%s) exported, status=sent",
                        task.id,
                        task.external_id,
                    )
                else:
                    logger.warning(
                        "Task %s (external_id=%s) export failed, status=done (will retry)",
                        task.id,
                        task.external_id,
                    )
            except Exception as exc:
                logger.exception(
                    "Task %s (external_id=%s) export error: %s",
                    task.id,
                    task.external_id,
                    exc,
                )
    finally:
        db.close()


def reset_stuck_job() -> None:
    db = SessionLocal()
    try:
        count = reset_stuck(db)
        if count > 0:
            logger.info("Reset %d stuck task(s): status processing -> pending", count)
    finally:
        db.close()


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        process_pending,
        "interval",
        seconds=settings.POLL_INTERVAL,
        id="process_pending",
    )
    scheduler.add_job(
        export_done,
        "interval",
        seconds=settings.POLL_INTERVAL,
        id="export_done",
    )
    scheduler.add_job(
        reset_stuck_job,
        "interval",
        seconds=60,
        id="reset_stuck",
    )
    scheduler.start()
    logger.info(
        "Scheduler started: process_pending and export_done every %ds, reset_stuck every 60s",
        settings.POLL_INTERVAL,
    )
    return scheduler

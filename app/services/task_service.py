import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.database_models import Task

logger = logging.getLogger(__name__)


def create_task(db: Session, external_id: str, input_text: str) -> Task:
    existing = db.query(Task).filter(Task.external_id == external_id).first()
    if existing:
        return existing

    task = Task(external_id=external_id, input_text=input_text, status="pending")
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def claim_one_pending(db: Session) -> Task | None:
    task = (
        db.query(Task)
        .filter(Task.status == "pending")
        .order_by(Task.created_at)
        .with_for_update(skip_locked=True)
        .first()
    )
    if task is None:
        return None

    task.status = "processing"
    db.commit()
    db.refresh(task)
    return task


def mark_done(db: Session, task: Task, result: str) -> None:
    task.status = "done"
    task.result = result
    task.error = None
    db.commit()


def mark_failed_or_retry(db: Session, task: Task, error_msg: str) -> None:
    task.attempts += 1
    task.error = error_msg
    if task.attempts >= settings.MAX_ATTEMPTS:
        task.status = "failed"
    else:
        task.status = "pending"
    db.commit()


def list_done_for_export(db: Session) -> list[Task]:
    return db.query(Task).filter(Task.status == "done").all()


def mark_sent(db: Session, task: Task) -> None:
    task.status = "sent"
    db.commit()


def reset_stuck(db: Session) -> int:
    cutoff = datetime.utcnow() - timedelta(minutes=settings.STUCK_MINUTES)
    stuck_tasks = (
        db.query(Task)
        .filter(Task.status == "processing", Task.updated_at < cutoff)
        .all()
    )
    for task in stuck_tasks:
        task.status = "pending"
    if stuck_tasks:
        db.commit()
    return len(stuck_tasks)


def list_tasks(db: Session) -> list[Task]:
    return db.query(Task).order_by(Task.created_at.desc()).all()

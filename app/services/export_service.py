import logging

import httpx

from app.core.config import settings
from app.models.database_models import Task

logger = logging.getLogger(__name__)


def send_result(task: Task) -> bool:
    payload = {"external_id": task.external_id, "result": task.result}

    if settings.TEST_MODE or not settings.RESULT_URL:
        logger.info("Export skipped (test mode or empty RESULT_URL): %s", payload)
        return True

    try:
        response = httpx.post(settings.RESULT_URL, json=payload, timeout=10)
        return response.is_success
    except httpx.HTTPError as exc:
        logger.error("Export failed for task %s: %s", task.external_id, exc)
        return False

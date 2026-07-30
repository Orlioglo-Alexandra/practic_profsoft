from uuid import uuid4

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.models.schemas import TaskCreate, TaskOut
from app.services.task_service import create_task, list_tasks

router = APIRouter(prefix="/tasks")


@router.post("", response_model=TaskOut)
def import_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = create_task(db, payload.external_id, payload.input_text)
    return task


@router.post("/mock", response_model=TaskOut)
def create_mock_task(db: Session = Depends(get_db)):
    if settings.API_URL:
        try:
            response = httpx.get(settings.API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            external_id = data["external_id"]
            input_text = data["input_text"]
        except (httpx.HTTPError, KeyError, TypeError) as exc:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to import task from API_URL: {exc}",
            ) from exc
    else:
        external_id = f"mock_{uuid4()}"
        input_text = "Отличный сервис, очень доволен!"

    task = create_task(db, external_id, input_text)
    return task

@router.get("/mock-api/task")
def mock_api_task():
    return {
        "external_id": "api_rev_001",
        "input_text": "Ужасное обслуживание, больше не приду"
    }

@router.get("", response_model=list[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return list_tasks(db)

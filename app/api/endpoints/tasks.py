from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
    task = create_task(
        db,
        external_id=f"mock_{uuid4()}",
        input_text="Отличный сервис, очень доволен!",
    )
    return task


@router.get("", response_model=list[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return list_tasks(db)

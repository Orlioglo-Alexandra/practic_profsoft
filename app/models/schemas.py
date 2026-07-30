from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str
    status: str
    result: str | None
    input_text: str | None
    attempts: int
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    external_id: str
    input_text: str

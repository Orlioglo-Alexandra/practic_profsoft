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


class DocumentCreate(BaseModel):
    source: str
    text: str


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    status: str
    attempts: int
    error: str | None
    created_at: datetime
    updated_at: datetime


class AskRequest(BaseModel):
    question: str


class SourceOut(BaseModel):
    source: str | None = None
    doc_id: int | None = None
    section: int | None = None
    score: float | None = None
    text: str | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceOut]

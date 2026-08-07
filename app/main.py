from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import ask, documents, health, tasks
from app.core.config import settings
from app.db.database import Base, SessionLocal, engine
from app.models import database_models  # noqa: F401 — регистрация моделей для create_all
from app.models.database_models import Document
from app.vector.qdrant_client import ensure_collection
from app.workers.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    recreated = ensure_collection()
    if recreated:
        db = SessionLocal()
        try:
            db.query(Document).filter(
                Document.status.in_(["indexed", "syncing", "failed"])
            ).update(
                {"status": "idle", "attempts": 0, "error": None},
                synchronize_session=False,
            )
            db.commit()
        finally:
            db.close()

    scheduler = None
    if settings.RUN_WORKER:
        scheduler = start_scheduler()

    yield

    if scheduler is not None:
        scheduler.shutdown()


app = FastAPI(title="AI microservice skeleton", lifespan=lifespan)

app.include_router(health.router)
app.include_router(tasks.router)
app.include_router(documents.router)
app.include_router(ask.router)

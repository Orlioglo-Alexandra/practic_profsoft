from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import ask, documents, health, tasks
from app.core.config import settings
from app.db.database import Base, engine
from app.models import database_models  # noqa: F401 — регистрация моделей для create_all
from app.vector.qdrant_client import ensure_collection
from app.workers.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ensure_collection()

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

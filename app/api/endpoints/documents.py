from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.database_models import Document
from app.models.schemas import DocumentCreate, DocumentOut
from app.services.index_service import create_document

router = APIRouter(prefix="/documents")


@router.post("", response_model=DocumentOut)
def enqueue_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    document = create_document(db, payload.source, payload.text)
    return document


@router.get("")
def get_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.id.desc()).all()
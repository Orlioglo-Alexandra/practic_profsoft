from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True)
    status = Column(String, default="pending")
    result = Column(Text, nullable=True)
    input_text = Column(Text, nullable=True)
    attempts = Column(Integer, default=0, nullable=False)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    status = Column(String, default="idle")  # idle|syncing|indexed|failed
    attempts = Column(Integer, default=0, nullable=False)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

"""SQLAlchemy database base and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from src.config import get_settings

settings = get_settings()

# Create SQLAlchemy engine
# For SQLite, we need to enable foreign keys and set check_same_thread=False for FastAPI
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.debug,  # Log SQL queries in debug mode
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    
    Usage in FastAPI:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database by creating all tables."""
    # Import all models here to ensure they're registered with Base
    from src.models import (
        User, Subject, Document, DocumentChunk, Chapter,
        Topic, TopicDependency, Note, Cheatsheet,
        PreviousYearQuestion, Flashcard, Timetable,
        TimetableSlot, UserProgress
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created successfully")

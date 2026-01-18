"""Subject service for business logic."""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from src.models import Subject, Chapter, Topic, Document
from src.api.schemas.subject import SubjectCreate, SubjectUpdate


def create_subject(db: Session, subject_data: SubjectCreate, user_id: str) -> Subject:
    """Create a new subject."""
    subject = Subject(
        user_id=user_id,
        **subject_data.model_dump()
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


def get_subject(db: Session, subject_id: str, user_id: str) -> Optional[Subject]:
    """Get a subject by ID for a specific user."""
    return db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == user_id
    ).first()


def get_subjects(
    db: Session,
    user_id: str,
    skip: int = 0,
    limit: int = 100
) -> tuple[list[Subject], int]:
    """Get all subjects for a user with pagination."""
    query = db.query(Subject).filter(Subject.user_id == user_id)
    
    total = query.count()
    subjects = query.offset(skip).limit(limit).all()
    
    return subjects, total


def update_subject(
    db: Session,
    subject: Subject,
    subject_data: SubjectUpdate
) -> Subject:
    """Update a subject."""
    update_data = subject_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(subject, field, value)
    
    db.commit()
    db.refresh(subject)
    return subject


def delete_subject(db: Session, subject: Subject) -> None:
    """Delete a subject."""
    db.delete(subject)
    db.commit()


def enrich_subject_response(db: Session, subject: Subject) -> dict:
    """Enrich subject with computed fields."""
    # Count chapters
    chapters_count = db.query(func.count(Chapter.id)).filter(
        Chapter.subject_id == subject.id
    ).scalar()
    
    # Count topics
    topics_count = db.query(func.count(Topic.id)).join(
        Chapter, Chapter.id == Topic.chapter_id
    ).filter(
        Chapter.subject_id == subject.id
    ).scalar()
    
    # Count documents
    documents_count = db.query(func.count(Document.id)).filter(
        Document.subject_id == subject.id
    ).scalar()
    
    return {
        **subject.__dict__,
        "chapters_count": chapters_count or 0,
        "topics_count": topics_count or 0,
        "documents_count": documents_count or 0,
    }

"""API dependencies."""
from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.base import get_db
from src.models import Subject, Document, User
from src.api.exceptions import NotFoundException


def get_current_user_id() -> str:
    """
    Get current user ID.
    
    TODO: Implement proper authentication in Phase 2.
    For now, return demo user ID from seed data.
    """
    # Hardcoded demo user ID for development
    # In production, this would validate JWT token and return actual user ID
    return "demo_user_id"


def get_subject_or_404(
    subject_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
) -> Subject:
    """Get subject by ID or raise 404."""
    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == user_id
    ).first()
    
    if not subject:
        raise NotFoundException(f"Subject with ID {subject_id} not found")
    
    return subject


def get_document_or_404(
    document_id: str,
    db: Session = Depends(get_db)
) -> Document:
    """Get document by ID or raise 404."""
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise NotFoundException(f"Document with ID {document_id} not found")
    
    return document

"""Document service for business logic."""
from sqlalchemy.orm import Session
from fastapi import UploadFile
from typing import Optional
from pathlib import Path

from src.models import Document
from src.utils.file_storage import save_upload_file, delete_file, get_file_extension


async def create_document(
    db: Session,
    file: UploadFile,
    subject_id: str
) -> Document:
    """
    Create a new document by uploading file.
    
    Args:
        db: Database session
        file: Uploaded file
        subject_id: Subject ID
        
    Returns:
        Created document
    """
    # Save file to storage
    file_path, file_size = await save_upload_file(file, subject_id)
    
    # Determine file type
    file_type = get_file_extension(file.filename or "file.pdf")
    
    # Create document record
    document = Document(
        subject_id=subject_id,
        filename=file.filename,
        file_type=file_type,
        file_path=str(file_path),
        file_size=file_size,
        processing_status="pending"
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return document


def get_document(db: Session, document_id: str) -> Optional[Document]:
    """Get a document by ID."""
    return db.query(Document).filter(Document.id == document_id).first()


def get_documents(
    db: Session,
    subject_id: str,
    skip: int = 0,
    limit: int = 100
) -> tuple[list[Document], int]:
    """Get all documents for a subject with pagination."""
    query = db.query(Document).filter(Document.subject_id == subject_id)
    
    total = query.count()
    documents = query.offset(skip).limit(limit).all()
    
    return documents, total


def delete_document(db: Session, document: Document) -> None:
    """
    Delete a document and its file.
    
    Args:
        db: Database session
        document: Document to delete
    """
    # Delete file from storage
    delete_file(document.file_path)
    
    # Delete document record
    db.delete(document)
    db.commit()

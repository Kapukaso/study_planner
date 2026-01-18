"""Document router."""
from fastapi import APIRouter, Depends, File, UploadFile, Form, status
from sqlalchemy.orm import Session

from src.database.base import get_db
from src.api.schemas import (
    DocumentUploadResponse,
    DocumentResponse,
    DocumentListResponse,
    MessageResponse
)
from src.api.dependencies import get_document_or_404, get_subject_or_404
from src.api.exceptions import BadRequestException
from src.services import document_service
from src.utils.file_storage import validate_file_type, get_file_size_mb
from src.models import Document, Subject

router = APIRouter()


@router.post("/documents/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(..., description="Document file (PDF, DOCX, PPT, images)"),
    subject_id: str = Form(..., description="Subject ID"),
    db: Session = Depends(get_db)
):
    """
    Upload a document for a subject.
    
    Supported file types:
    - PDF (.pdf)
    - Word (.docx, .doc)
    - PowerPoint (.pptx, .ppt)
    - Images (.png, .jpg, .jpeg)
    
    Maximum file size: 50 MB
    """
    # Validate subject exists
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise BadRequestException(f"Subject with ID {subject_id} not found")
    
    # Validate file type
    is_valid, file_type = validate_file_type(file.filename or "")
    if not is_valid:
        raise BadRequestException(
            f"Unsupported file type. Allowed: PDF, DOCX, PPT, PNG, JPG"
        )
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    max_size = 50 * 1024 * 1024  # 50 MB
    if file_size > max_size:
        raise BadRequestException(
            f"File too large. Maximum size: 50 MB. Your file: {get_file_size_mb(file_size)} MB"
        )
    
    # Create document
    document = await document_service.create_document(db, file, subject_id)
    
    return DocumentUploadResponse(**document.__dict__)


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents(
    subject_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all documents for a subject.
    
    - **subject_id**: Subject ID (required)
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    documents, total = document_service.get_documents(db, subject_id, skip, limit)
    
    return DocumentListResponse(
        documents=[DocumentResponse(**doc.__dict__) for doc in documents],
        total=total
    )


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document: Document = Depends(get_document_or_404)
):
    """
    Get a specific document by ID.
    
    Returns document details including processing status.
    """
    return DocumentResponse(**document.__dict__)


@router.delete("/documents/{document_id}", response_model=MessageResponse)
async def delete_document(
    document: Document = Depends(get_document_or_404),
    db: Session = Depends(get_db)
):
    """
    Delete a document.
    
    This will also delete the file from storage.
    """
    filename = document.filename
    document_service.delete_document(db, document)
    
    return MessageResponse(message=f"Document '{filename}' deleted successfully")

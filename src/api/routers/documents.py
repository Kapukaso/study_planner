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


# Import processing schemas
from src.api.schemas.chunk import (
    ProcessingResponse,
    ChunkResponse,
    ChunkListResponse,
    ChunkStatsResponse
)
from src.models import DocumentChunk
from src.services.processing_service import DocumentProcessor
from sqlalchemy import func


@router.post("/documents/{document_id}/process", response_model=ProcessingResponse)
async def process_document(
    document: Document = Depends(get_document_or_404),
    db: Session = Depends(get_db)
):
    """
    Process uploaded document: parse and classify content.
    
    This endpoint:
    1. Parses the document (PDF/DOCX/PPT)
    2. Extracts text chunks
    3. Classifies each chunk into content types
    4. Saves chunks to database
    """
    # Check if already processed
    if document.processing_status == 'completed':
        chunk_count = db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document.id
        ).count()
        
        return ProcessingResponse(
            document_id=document.id,
            status='completed',
            chunks_created=chunk_count,
            message=f"Document already processed with {chunk_count} chunks"
        )
    
    # Process document
    processor = DocumentProcessor()
    try:
        chunk_count = processor.process_document(db, document)
        
        return ProcessingResponse(
            document_id=document.id,
            status='completed',
            chunks_created=chunk_count,
            message=f"Successfully processed document into {chunk_count} chunks"
        )
    except Exception as e:
        return ProcessingResponse(
            document_id=document.id,
            status='failed',
            chunks_created=0,
            message=f"Processing failed: {str(e)}"
        )


@router.get("/documents/{document_id}/chunks", response_model=ChunkListResponse)
async def get_document_chunks(
    document_id: str,
    content_type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all chunks for a document.
    
    - **content_type**: Optional filter by content type (concept, formula, definition, example, pyq, highlight)
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    query = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id)
    
    # Filter by content type if specified
    if content_type:
        query = query.filter(DocumentChunk.content_type == content_type)
    
    # Order by chunk index
    query = query.order_by(DocumentChunk.chunk_index)
    
    total = query.count()
    chunks = query.offset(skip).limit(limit).all()
    
    return ChunkListResponse(
        chunks=[ChunkResponse(**chunk.__dict__) for chunk in chunks],
        total=total
    )


@router.get("/documents/{document_id}/chunks/stats", response_model=ChunkStatsResponse)
async def get_chunk_stats(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get statistics about chunks in a document.
    
    Returns counts by content type and average confidence score.
    """
    # Get chunks grouped by content type
    type_counts = db.query(
        DocumentChunk.content_type,
        func.count(DocumentChunk.id).label('count')
    ).filter(
        DocumentChunk.document_id == document_id
    ).group_by(DocumentChunk.content_type).all()
    
    by_type = {content_type: count for content_type, count in type_counts}
    total_chunks = sum(by_type.values())
    
    # Calculate average confidence
    avg_confidence = db.query(
        func.avg(DocumentChunk.confidence_score)
    ).filter(
        DocumentChunk.document_id == document_id
    ).scalar() or 0.0
    
    return ChunkStatsResponse(
        document_id=document_id,
        total_chunks=total_chunks,
        by_type=by_type,
        avg_confidence=round(avg_confidence, 2)
    )

"""Document Pydantic schemas."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DocumentUploadResponse(BaseModel):
    """Schema for document upload response."""
    id: str
    subject_id: str
    filename: str
    file_type: str
    file_size: int
    processing_status: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    """Schema for document response."""
    id: str
    subject_id: str
    filename: str
    file_type: str
    file_path: str
    file_size: int
    page_count: Optional[int]
    processing_status: str
    ocr_applied: bool
    uploaded_at: datetime
    processed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class DocumentStatusResponse(BaseModel):
    """Schema for document processing status."""
    id: str
    filename: str
    processing_status: str
    progress_percentage: int = 0
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Schema for list of documents."""
    documents: list[DocumentResponse]
    total: int

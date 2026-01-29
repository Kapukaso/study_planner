"""Document chunk Pydantic schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChunkResponse(BaseModel):
    """Schema for document chunk response."""
    id: str
    document_id: str
    chunk_index: int
    raw_text: str
    page_number: Optional[int]
    content_type: str
    confidence_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChunkListResponse(BaseModel):
    """Schema for list of chunks."""
    chunks: list[ChunkResponse]
    total: int


class ChunkStatsResponse(BaseModel):
    """Schema for chunk statistics."""
    document_id: str
    total_chunks: int
    by_type: dict[str, int]
    avg_confidence: float


class ProcessingResponse(BaseModel):
    """Schema for processing response."""
    document_id: str
    status: str
    chunks_created: int
    message: str

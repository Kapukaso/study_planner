"""Topic Pydantic schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Any


class TopicResponse(BaseModel):
    """Schema for topic response."""
    id: str
    chapter_id: str
    title: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    difficulty_score: Optional[float] = None
    estimated_hours: Optional[float] = None
    importance_score: Optional[float] = None
    pyq_frequency: Optional[int] = None
    keywords: Optional[Any] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TopicListResponse(BaseModel):
    """Schema for list of topics."""
    topics: List[TopicResponse]
    total: int

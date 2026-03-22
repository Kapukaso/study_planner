"""Resource Pydantic schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Any


class ResourceBase(BaseModel):
    """Base schema for resources."""
    topic_id: str


class NoteResponse(ResourceBase):
    """Schema for note response."""
    id: str
    content: str
    summary: Optional[str] = None
    examples: Optional[List[str]] = None
    generation_method: Optional[str] = None
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FlashcardResponse(ResourceBase):
    """Schema for flashcard response."""
    id: str
    question: str
    answer: str
    card_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PYQResponse(ResourceBase):
    """Schema for PYQ response."""
    id: str
    question_text: str
    answer_text: Optional[str] = None
    question_type: Optional[str] = None
    marks: Optional[int] = None
    year: Optional[int] = None
    source: Optional[str] = None
    difficulty: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CheatsheetResponse(ResourceBase):
    """Schema for cheatsheet response."""
    id: str
    content: str
    formulas: Optional[List[str]] = None
    key_definitions: Optional[List[str]] = None
    quick_tips: Optional[List[str]] = None
    format: str
    file_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TopicResourcesResponse(BaseModel):
    """Schema for all resources of a topic."""
    topic_id: str
    notes: List[NoteResponse]
    flashcards: List[FlashcardResponse]
    pyqs: List[PYQResponse]
    cheatsheets: List[CheatsheetResponse]

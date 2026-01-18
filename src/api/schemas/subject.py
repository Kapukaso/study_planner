"""Subject Pydantic schemas."""
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class SubjectCreate(BaseModel):
    """Schema for creating a subject."""
    name: str = Field(..., min_length=1, max_length=200, description="Subject name")
    code: Optional[str] = Field(None, max_length=50, description="Course code")
    exam_date: Optional[date] = Field(None, description="Final exam date")
    priority: int = Field(5, ge=1, le=10, description="Priority level (1-10)")
    total_marks: Optional[int] = Field(None, ge=0, description="Total marks for subject")


class SubjectUpdate(BaseModel):
    """Schema for updating a subject."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    code: Optional[str] = Field(None, max_length=50)
    exam_date: Optional[date] = None
    priority: Optional[int] = Field(None, ge=1, le=10)
    total_marks: Optional[int] = Field(None, ge=0)


class SubjectResponse(BaseModel):
    """Schema for subject response."""
    id: str
    user_id: str
    name: str
    code: Optional[str]
    exam_date: Optional[date]
    priority: int
    total_marks: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    # Computed fields
    chapters_count: int = 0
    topics_count: int = 0
    documents_count: int = 0
    
    class Config:
        from_attributes = True


class SubjectListResponse(BaseModel):
    """Schema for list of subjects."""
    subjects: list[SubjectResponse]
    total: int

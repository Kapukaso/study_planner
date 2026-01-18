"""Subject router."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.base import get_db
from src.api.schemas import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse,
    SubjectListResponse,
    MessageResponse
)
from src.api.dependencies import get_current_user_id, get_subject_or_404
from src.services import subject_service
from src.models import Subject

router = APIRouter()


@router.post("/subjects", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """
    Create a new subject.
    
    - **name**: Subject name (required)
    - **code**: Course code (optional)
    - **exam_date**: Final exam date (optional)
    - **priority**: Priority level 1-10 (default: 5)
    - **total_marks**: Total marks for subject (optional)
    """
    subject = subject_service.create_subject(db, subject_data, user_id)
    enriched = subject_service.enrich_subject_response(db, subject)
    return SubjectResponse(**enriched)


@router.get("/subjects", response_model=SubjectListResponse)
async def list_subjects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get all subjects for the current user.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    subjects, total = subject_service.get_subjects(db, user_id, skip, limit)
    
    # Enrich each subject with counts
    enriched_subjects = [
        SubjectResponse(**subject_service.enrich_subject_response(db, subject))
        for subject in subjects
    ]
    
    return SubjectListResponse(subjects=enriched_subjects, total=total)


@router.get("/subjects/{subject_id}", response_model=SubjectResponse)
async def get_subject(
    subject: Subject = Depends(get_subject_or_404),
    db: Session = Depends(get_db)
):
    """
    Get a specific subject by ID.
    
    Returns subject details with counts of chapters, topics, and documents.
    """
    enriched = subject_service.enrich_subject_response(db, subject)
    return SubjectResponse(**enriched)


@router.put("/subjects/{subject_id}", response_model=SubjectResponse)
async def update_subject(
    subject_data: SubjectUpdate,
    subject: Subject = Depends(get_subject_or_404),
    db: Session = Depends(get_db)
):
    """
    Update a subject.
    
    Only provided fields will be updated. All fields are optional.
    """
    updated_subject = subject_service.update_subject(db, subject, subject_data)
    enriched = subject_service.enrich_subject_response(db, updated_subject)
    return SubjectResponse(**enriched)


@router.delete("/subjects/{subject_id}", response_model=MessageResponse)
async def delete_subject(
    subject: Subject = Depends(get_subject_or_404),
    db: Session = Depends(get_db)
):
    """
    Delete a subject.
    
    This will also delete all associated chapters, topics, and documents.
    """
    subject_service.delete_subject(db, subject)
    return MessageResponse(message=f"Subject '{subject.name}' deleted successfully")

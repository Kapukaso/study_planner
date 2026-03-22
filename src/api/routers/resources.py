"""Resource router."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.database.base import get_db
from src.api.schemas import (
    NoteResponse,
    FlashcardResponse,
    PYQResponse,
    CheatsheetResponse,
    TopicResourcesResponse
)
from src.api.dependencies import get_topic_or_404
from src.models import Note, Flashcard, PreviousYearQuestion, Cheatsheet, Topic

router = APIRouter()


@router.get("/topics/{topic_id}/resources", response_model=TopicResourcesResponse)
async def get_topic_resources(
    topic: Topic = Depends(get_topic_or_404),
    db: Session = Depends(get_db)
):
    """
    Get all study resources (notes, flashcards, PYQs, cheatsheets) for a specific topic.
    """
    notes = db.query(Note).filter(Note.topic_id == topic.id).all()
    flashcards = db.query(Flashcard).filter(Flashcard.topic_id == topic.id).all()
    pyqs = db.query(PreviousYearQuestion).filter(PreviousYearQuestion.topic_id == topic.id).all()
    cheatsheets = db.query(Cheatsheet).filter(Cheatsheet.topic_id == topic.id).all()
    
    return TopicResourcesResponse(
        topic_id=topic.id,
        notes=[NoteResponse.model_validate(n) for n in notes],
        flashcards=[FlashcardResponse.model_validate(f) for f in flashcards],
        pyqs=[PYQResponse.model_validate(p) for p in pyqs],
        cheatsheets=[CheatsheetResponse.model_validate(c) for c in cheatsheets]
    )


@router.get("/topics/{topic_id}/notes", response_model=List[NoteResponse])
async def get_topic_notes(
    topic: Topic = Depends(get_topic_or_404),
    db: Session = Depends(get_db)
):
    """Get all notes for a topic."""
    notes = db.query(Note).filter(Note.topic_id == topic.id).all()
    return [NoteResponse.model_validate(n) for n in notes]


@router.get("/topics/{topic_id}/flashcards", response_model=List[FlashcardResponse])
async def get_topic_flashcards(
    topic: Topic = Depends(get_topic_or_404),
    db: Session = Depends(get_db)
):
    """Get all flashcards for a topic."""
    flashcards = db.query(Flashcard).filter(Flashcard.topic_id == topic.id).all()
    return [FlashcardResponse.model_validate(f) for f in flashcards]


@router.get("/topics/{topic_id}/pyqs", response_model=List[PYQResponse])
async def get_topic_pyqs(
    topic: Topic = Depends(get_topic_or_404),
    db: Session = Depends(get_db)
):
    """Get all PYQs for a topic."""
    pyqs = db.query(PreviousYearQuestion).filter(PreviousYearQuestion.topic_id == topic.id).all()
    return [PYQResponse.model_validate(p) for p in pyqs]


@router.get("/topics/{topic_id}/cheatsheets", response_model=List[CheatsheetResponse])
async def get_topic_cheatsheets(
    topic: Topic = Depends(get_topic_or_404),
    db: Session = Depends(get_db)
):
    """Get all cheatsheets for a topic."""
    cheatsheets = db.query(Cheatsheet).filter(Cheatsheet.topic_id == topic.id).all()
    return [CheatsheetResponse.model_validate(c) for c in cheatsheets]

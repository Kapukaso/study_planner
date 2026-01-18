"""Flashcard model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from src.database.base import Base


class Flashcard(Base):
    """Flashcard model for active recall practice."""
    
    __tablename__ = "flashcards"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Card Content
    question = Column(Text, nullable=False)  # Front of card
    answer = Column(Text, nullable=False)  # Back of card
    
    # Card Type
    card_type = Column(String(50))  # concept, definition, formula, application
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    topic = relationship("Topic", back_populates="flashcards")
    
    def __repr__(self):
        return f"<Flashcard(id={self.id}, type={self.card_type})>"

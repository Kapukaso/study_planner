"""Previous Year Question (PYQ) model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from src.database.base import Base


class PreviousYearQuestion(Base):
    """Previous Year Question model."""
    
    __tablename__ = "pyqs"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Question Content
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text)  # Optional solution/answer
    
    # Question Metadata
    question_type = Column(String(50))  # mcq, short_answer, long_answer, numerical
    marks = Column(Integer)  # Total marks for question
    year = Column(Integer, index=True)  # Exam year
    source = Column(String(255))  # Source exam/document
    difficulty = Column(String(20), index=True)  # easy, medium, hard
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    topic = relationship("Topic", back_populates="pyqs")
    
    def __repr__(self):
        return f"<PYQ(id={self.id}, year={self.year}, marks={self.marks}, difficulty={self.difficulty})>"

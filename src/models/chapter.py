"""Chapter model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from src.database.base import Base


class Chapter(Base):
    """Chapter model - organizational unit within a subject."""
    
    __tablename__ = "chapters"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    subject_id = Column(String(36), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Chapter Information
    title = Column(String(255), nullable=False)
    chapter_number = Column(Integer)
    description = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    subject = relationship("Subject", back_populates="chapters")
    topics = relationship("Topic", back_populates="chapter", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Chapter(id={self.id}, title={self.title}, number={self.chapter_number})>"

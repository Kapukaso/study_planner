"""Topic model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DECIMAL, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator

from src.database.base import Base


# Type adapter for ARRAY that falls back to JSON list for SQLite
class ArrayType(TypeDecorator):
    """Array type that works with both PostgreSQL and SQLite."""
    impl = Text
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(ARRAY(Text))
        else:
            return dialect.type_descriptor(Text())
    
    def process_bind_param(self, value, dialect):
        if dialect.name != 'postgresql' and value is not None:
            # For SQLite, store as comma-separated string
            return ','.join(value) if isinstance(value, list) else value
        return value
    
    def process_result_value(self, value, dialect):
        if dialect.name != 'postgresql' and value is not None:
            # For SQLite, parse comma-separated string
            return value.split(',') if value else []
        return value


class Topic(Base):
    """Topic model - core knowledge units."""
    
    __tablename__ = "topics"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    chapter_id = Column(String(36), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Topic Information
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Difficulty & Time Estimation
    difficulty = Column(String(20), index=True)  # easy, medium, hard
    difficulty_score = Column(DECIMAL(3, 2))  # 0.00 - 1.00
    estimated_hours = Column(DECIMAL(4, 1))  # e.g., 2.5 hours
    importance_score = Column(DECIMAL(3, 2))  # 0.00 - 1.00
    pyq_frequency = Column(Integer, default=0)  # How often it appears in PYQs
    
    # Keywords/Tags
    keywords = Column(ArrayType)  # PostgreSQL array or comma-separated for SQLite
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="topics")
    
    # Dependencies
    dependencies = relationship(
        "TopicDependency",
        foreign_keys="TopicDependency.topic_id",
        back_populates="topic",
        cascade="all, delete-orphan"
    )
    required_by = relationship(
        "TopicDependency",
        foreign_keys="TopicDependency.depends_on_topic_id",
        back_populates="depends_on_topic"
    )
    
    # Resources
    notes = relationship("Note", back_populates="topic", cascade="all, delete-orphan")
    cheatsheets = relationship("Cheatsheet", back_populates="topic", cascade="all, delete-orphan")
    pyqs = relationship("PreviousYearQuestion", back_populates="topic", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="topic", cascade="all, delete-orphan")
    
    # Scheduling
    timetable_slots = relationship("TimetableSlot", back_populates="topic")
    
    # Progress tracking
    progress_records = relationship("UserProgress", back_populates="topic", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Topic(id={self.id}, title={self.title}, difficulty={self.difficulty})>"

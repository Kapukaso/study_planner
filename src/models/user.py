"""User model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DECIMAL, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, JSON

from src.database.base import Base


# Type adapter for JSONB that falls back to JSON for SQLite
class JSONBType(TypeDecorator):
    """JSONB type that works with both PostgreSQL and SQLite."""
    impl = JSON
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(JSONB())
        else:
            return dialect.type_descriptor(JSON())


class User(Base):
    """User model for storing user accounts and preferences."""
    
    __tablename__ = "users"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    full_name = Column(String(255))
    
    # Study Preferences
    daily_study_hours = Column(DECIMAL(3, 1), default=4.0)
    preferred_study_times = Column(JSONBType)  # e.g., [{"start": "09:00", "end": "12:00"}, ...]
    learning_style = Column(String(50))  # visual, auditory, kinesthetic
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    subjects = relationship("Subject", back_populates="user", cascade="all, delete-orphan")
    timetables = relationship("Timetable", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

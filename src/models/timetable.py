"""Timetable model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship

from src.database.base import Base


class Timetable(Base):
    """Timetable model for generated study schedules."""
    
    __tablename__ = "timetables"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Timetable Information
    name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(20), default="active", index=True)  # active, completed, archived
    total_hours_allocated = Column(DECIMAL(6, 1))  # Total study hours
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="timetables")
    slots = relationship("TimetableSlot", back_populates="timetable", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Timetable(id={self.id}, name={self.name}, status={self.status})>"

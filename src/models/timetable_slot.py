"""Timetable slot model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, Time, ForeignKey, DECIMAL, Text, DateTime
from sqlalchemy.orm import relationship

from src.database.base import Base


class TimetableSlot(Base):
    """Timetable slot model for individual study sessions."""
    
    __tablename__ = "timetable_slots"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    timetable_id = Column(String(36), ForeignKey("timetables.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="SET NULL"), index=True)
    
    # Schedule Information
    date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration_hours = Column(DECIMAL(3, 1), nullable=False)
    
    # Slot Type & Status
    slot_type = Column(String(50), default="study")  # study, revision, pyq_practice, break
    status = Column(String(20), default="pending", index=True)  # pending, completed, skipped, rescheduled
    
    # User Notes
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)
    
    # Relationships
    timetable = relationship("Timetable", back_populates="slots")
    topic = relationship("Topic", back_populates="timetable_slots")
    
    def __repr__(self):
        return f"<TimetableSlot(id={self.id}, date={self.date}, type={self.slot_type}, status={self.status})>"

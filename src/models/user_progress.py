"""User progress model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DECIMAL, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from src.database.base import Base


class UserProgress(Base):
    """User progress model for tracking topic mastery."""
    
    __tablename__ = "user_progress"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Progress Information
    status = Column(String(50), default="not_started", index=True)  # not_started, in_progress, completed, needs_revision
    progress_percentage = Column(Integer, default=0)  # 0-100
    time_spent_hours = Column(DECIMAL(5, 1), default=0.0)
    
    # PYQ Performance
    pyqs_attempted = Column(Integer, default=0)
    pyqs_correct = Column(Integer, default=0)
    
    # Mastery
    mastery_level = Column(String(20))  # beginner, intermediate, advanced, expert
    last_studied_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="progress")
    topic = relationship("Topic", back_populates="progress_records")
    
    # Table constraints - one progress record per user-topic pair
    __table_args__ = (
        UniqueConstraint('user_id', 'topic_id', name='uq_user_topic_progress'),
    )
    
    def __repr__(self):
        return f"<UserProgress(user={self.user_id}, topic={self.topic_id}, status={self.status}, progress={self.progress_percentage}%)>"

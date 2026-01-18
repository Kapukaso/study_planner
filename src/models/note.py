"""Note model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.models.user import JSONBType


class Note(Base):
    """Note model for auto-generated study notes."""
    
    __tablename__ = "notes"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Content
    content = Column(Text, nullable=False)  # Markdown format
    summary = Column(Text)  # Brief summary
    examples = Column(JSONBType)  # Extracted examples as JSON
    
    # Metadata
    generation_method = Column(String(50))  # extraction, ai_generated, manual
    version = Column(Integer, default=1)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    topic = relationship("Topic", back_populates="notes")
    
    def __repr__(self):
        return f"<Note(id={self.id}, topic_id={self.topic_id}, method={self.generation_method})>"

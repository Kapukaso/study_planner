"""Cheatsheet model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.models.user import JSONBType
from src.models.topic import ArrayType


class Cheatsheet(Base):
    """Cheatsheet model for one-page summaries."""
    
    __tablename__ = "cheatsheets"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Content
    content = Column(Text, nullable=False)  # Main content in Markdown
    formulas = Column(JSONBType)  # Extracted formulas as JSON
    key_definitions = Column(JSONBType)  # Key definitions as JSON
    quick_tips = Column(ArrayType)  # Quick tips array
    
    # Format & Storage
    format = Column(String(20), default="markdown")  # markdown, pdf, html
    file_path = Column(Text)  # Path to generated file (if PDF/HTML)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    topic = relationship("Topic", back_populates="cheatsheets")
    
    def __repr__(self):
        return f"<Cheatsheet(id={self.id}, topic_id={self.topic_id}, format={self.format})>"

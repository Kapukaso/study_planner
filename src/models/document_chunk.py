"""Document chunk model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DECIMAL, DateTime
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.models.user import JSONBType


class DocumentChunk(Base):
    """Document chunk model for parsed text segments."""
    
    __tablename__ = "document_chunks"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Chunk Information
    chunk_index = Column(Integer, nullable=False)  # Order in document
    raw_text = Column(Text, nullable=False)
    page_number = Column(Integer)
    
    # Content Classification
    content_type = Column(String(50), index=True)  # concept, formula, definition, example, pyq, highlight
    confidence_score = Column(DECIMAL(3, 2))  # 0-1
    
    # Additional Metadata
    chunk_metadata = Column(JSONBType)  # font info, position, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    
    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, type={self.content_type}, page={self.page_number})>"

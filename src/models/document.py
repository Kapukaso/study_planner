"""Document model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.database.base import Base


class Document(Base):
    """Document model for uploaded files."""
    
    __tablename__ = "documents"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    subject_id = Column(String(36), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # File Metadata
    filename = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)  # pdf, docx, ppt, image
    file_path = Column(Text, nullable=False)
    file_size = Column(BigInteger)  # in bytes
    page_count = Column(Integer)
    
    # Processing Status
    processing_status = Column(String(50), default="pending", index=True)  # pending, processing, completed, failed
    ocr_applied = Column(Boolean, default=False)
    
    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime)
    
    # Relationships
    subject = relationship("Subject", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename}, status={self.processing_status})>"

"""Subject model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from src.database.base import Base


class Subject(Base):
    """Subject/Course model."""
    
    __tablename__ = "subjects"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Subject Information
    name = Column(String(200), nullable=False)  # e.g., "Operating Systems"
    code = Column(String(50))  # e.g., "CS301"
    exam_date = Column(Date, index=True)
    priority = Column(Integer, default=5)  # 1-10 scale
    total_marks = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="subjects")
    documents = relationship("Document", back_populates="subject", cascade="all, delete-orphan")
    chapters = relationship("Chapter", back_populates="subject", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Subject(id={self.id}, name={self.name}, code={self.code})>"

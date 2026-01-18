"""Topic dependency model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from src.database.base import Base


class TopicDependency(Base):
    """Topic dependency model for prerequisite relationships."""
    
    __tablename__ = "topic_dependencies"
    
    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    depends_on_topic_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Dependency Strength
    strength = Column(String(20), default="required")  # required, recommended, related
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    topic = relationship("Topic", foreign_keys=[topic_id], back_populates="dependencies")
    depends_on_topic = relationship("Topic", foreign_keys=[depends_on_topic_id], back_populates="required_by")
    
    # Table constraints
    __table_args__ = (
        UniqueConstraint('topic_id', 'depends_on_topic_id', name='uq_topic_dependency'),
        CheckConstraint('topic_id != depends_on_topic_id', name='ck_no_self_dependency'),
    )
    
    def __repr__(self):
        return f"<TopicDependency(topic={self.topic_id}, depends_on={self.depends_on_topic_id}, strength={self.strength})>"

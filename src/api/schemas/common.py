"""Common Pydantic schemas."""
from pydantic import BaseModel
from datetime import datetime


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    status_code: int
    timestamp: datetime = datetime.utcnow()


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    skip: int = 0
    limit: int = 100

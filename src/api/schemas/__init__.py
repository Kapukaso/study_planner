"""API schemas package."""
from src.api.schemas.common import ErrorResponse, MessageResponse, PaginationParams
from src.api.schemas.subject import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse,
    SubjectListResponse
)
from src.api.schemas.document import (
    DocumentUploadResponse,
    DocumentResponse,
    DocumentStatusResponse,
    DocumentListResponse
)

__all__ = [
    "ErrorResponse",
    "MessageResponse",
    "PaginationParams",
    "SubjectCreate",
    "SubjectUpdate",
    "SubjectResponse",
    "SubjectListResponse",
    "DocumentUploadResponse",
    "DocumentResponse",
    "DocumentStatusResponse",
    "DocumentListResponse",
]

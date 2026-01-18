"""File storage utilities."""
import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from typing import Tuple

from src.config import get_settings

settings = get_settings()

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "doc": "application/msword",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "ppt": "application/vnd.ms-powerpoint",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
}


def ensure_upload_dir() -> Path:
    """Ensure upload directory exists."""
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    return Path(filename).suffix.lstrip('.').lower()


def validate_file_type(filename: str) -> Tuple[bool, str]:
    """
    Validate file type.
    
    Returns:
        Tuple of (is_valid, file_type)
    """
    extension = get_file_extension(filename)
    
    if extension in ALLOWED_EXTENSIONS:
        return True, extension
    
    return False, ""


async def save_upload_file(file: UploadFile, subject_id: str) -> Tuple[Path, int]:
    """
    Save uploaded file to storage.
    
    Args:
        file: Uploaded file
        subject_id: Subject ID for organization
        
    Returns:
        Tuple of (file_path, file_size)
    """
    # Ensure upload directory exists
    upload_dir = ensure_upload_dir()
    
    # Create subject-specific directory
    subject_dir = upload_dir / subject_id
    subject_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    extension = get_file_extension(file.filename or "file.pdf")
    unique_filename = f"{uuid.uuid4()}.{extension}"
    file_path = subject_dir / unique_filename
    
    # Save file
    file_size = 0
    with open(file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):  # Read 1MB at a time
            buffer.write(chunk)
            file_size += len(chunk)
    
    return file_path, file_size


def delete_file(file_path: str) -> bool:
    """
    Delete file from storage.
    
    Returns:
        True if file was deleted, False if file didn't exist
    """
    path = Path(file_path)
    if path.exists():
        path.unlink()
        return True
    return False


def get_file_size_mb(size_bytes: int) -> float:
    """Convert file size from bytes to MB."""
    return round(size_bytes / (1024 * 1024), 2)

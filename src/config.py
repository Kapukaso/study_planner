"""Application configuration module."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "sqlite:///./study_planner.db"
    
    # Application
    app_name: str = "Study Planner System"
    debug: bool = True
    secret_key: str = "dev-secret-key-change-in-production"
    
    # File Storage
    upload_dir: Path = Path("./uploads")
    max_upload_size_mb: int = 50
    
    # Tesseract OCR (if installed)
    tesseract_cmd: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

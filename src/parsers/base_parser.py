"""Base parser interface and common utilities."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import re
import os
from src.parsers.exceptions import FileNotReadableError, UnsupportedFormatError


class ParsedChunk:
    """Represents a parsed text chunk."""
    
    def __init__(
        self,
        text: str,
        page_number: int = None,
        chunk_index: int = 0,
        metadata: Dict[str, Any] = None
    ):
        self.text = text
        self.page_number = page_number
        self.chunk_index = chunk_index
        self.metadata = metadata or {}


class BaseParser(ABC):
    """Base class for document parsers."""
    
    def validate_file(self, file_path: str, expected_extensions: List[str]):
        """Validate if file exists and has correct extension."""
        if not os.path.exists(file_path):
            raise FileNotReadableError(f"File not found: {file_path}")
        
        if not os.access(file_path, os.R_OK):
            raise FileNotReadableError(f"File is not readable: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in expected_extensions:
            raise UnsupportedFormatError(
                f"Unsupported file format: {ext}. Expected: {', '.join(expected_extensions)}"
            )

    @abstractmethod
    def parse(self, file_path: str) -> List[ParsedChunk]:
        """
        Parse document and return list of chunks.
        
        Args:
            file_path: Path to document file
            
        Returns:
            List of ParsedChunk objects
        """
        pass
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = text.strip()
        
        return text
    
    @staticmethod
    def chunk_by_paragraphs(text: str, max_chunk_size: int = 1000) -> List[str]:
        """
        Split text into chunks by paragraphs.
        
        Args:
            text: Text to split
            max_chunk_size: Maximum characters per chunk
            
        Returns:
            List of text chunks
        """
        # Split by double newlines (paragraphs)
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # If adding this paragraph exceeds max size, save current chunk
            if len(current_chunk) + len(para) > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                current_chunk += "\n\n" + para if current_chunk else para
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

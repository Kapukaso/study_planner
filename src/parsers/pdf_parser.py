"""PDF parser using pdfplumber."""
import pdfplumber
from pathlib import Path
from typing import List

from src.parsers.base_parser import BaseParser, ParsedChunk


class PDFParser(BaseParser):
    """Parser for PDF documents."""
    
    def parse(self, file_path: str) -> List[ParsedChunk]:
        """
        Parse PDF document and extract text by pages.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            List of ParsedChunk objects, one per page
        """
        chunks = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extract text from page
                    text = page.extract_text()
                    
                    if text:
                        # Clean text
                        cleaned_text = self.clean_text(text)
                        
                        if cleaned_text:
                            # Create chunk with page metadata
                            chunk = ParsedChunk(
                                text=cleaned_text,
                                page_number=page_num,
                                chunk_index=page_num - 1,
                                metadata={
                                    'page_width': page.width,
                                    'page_height': page.height,
                                    'parser': 'pdfplumber'
                                }
                            )
                            chunks.append(chunk)
        
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")
        
        return chunks
    
    def get_page_text(self, file_path: str, page_number: int) -> str:
        """
        Get text from a specific page.
        
        Args:
            file_path: Path to PDF file
            page_number: Page number (1-indexed)
            
        Returns:
            Text content of the page
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                if 0 < page_number <= len(pdf.pages):
                    page = pdf.pages[page_number - 1]
                    text = page.extract_text()
                    return self.clean_text(text) if text else ""
                return ""
        except Exception as e:
            raise ValueError(f"Error reading page {page_number}: {str(e)}")
    
    def get_page_count(self, file_path: str) -> int:
        """Get total number of pages in PDF."""
        try:
            with pdfplumber.open(file_path) as pdf:
                return len(pdf.pages)
        except Exception:
            return 0

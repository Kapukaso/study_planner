"""DOCX parser using python-docx."""
from docx import Document
from typing import List

from src.parsers.base_parser import BaseParser, ParsedChunk


class DOCXParser(BaseParser):
    """Parser for DOCX documents."""
    
    def parse(self, file_path: str) -> List[ParsedChunk]:
        """
        Parse DOCX document and extract text.
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            List of ParsedChunk objects
        """
        chunks = []
        
        try:
            doc = Document(file_path)
            
            # Extract all paragraphs
            all_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    all_text.append(para.text.strip())
            
            # Join and chunk by paragraphs
            full_text = '\n\n'.join(all_text)
            text_chunks = self.chunk_by_paragraphs(full_text)
            
            # Create ParsedChunk objects
            for idx, text_chunk in enumerate(text_chunks):
                chunk = ParsedChunk(
                    text=text_chunk,
                    page_number=None,  # DOCX doesn't have pages
                    chunk_index=idx,
                    metadata={
                        'paragraph_count': len(all_text),
                        'parser': 'python-docx'
                    }
                )
                chunks.append(chunk)
        
        except Exception as e:
            raise ValueError(f"Error parsing DOCX: {str(e)}")
        
        return chunks
    
    def extract_headings(self, file_path: str) -> List[str]:
        """
        Extract all headings from document.
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            List of heading texts
        """
        try:
            doc = Document(file_path)
            headings = []
            
            for para in doc.paragraphs:
                if para.style.name.startswith('Heading'):
                    headings.append(para.text.strip())
            
            return headings
        except Exception:
            return []

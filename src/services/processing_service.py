"""Document processing service - orchestrates parsing and classification."""
from sqlalchemy.orm import Session
from typing import List

from src.models import Document, DocumentChunk
from src.parsers import PDFParser, DOCXParser, PPTParser, ImageParser
from src.classifier import ContentClassifier


class DocumentProcessor:
    """Handles document parsing and content classification."""
    
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.docx_parser = DOCXParser()
        self.ppt_parser = PPTParser()
        self.image_parser = ImageParser()
        self.classifier = ContentClassifier()
    
    def process_document(self, db: Session, document: Document) -> int:
        """
        Process document: parse, classify, and save chunks.
        
        Args:
            db: Database session
            document: Document model to process
            
        Returns:
            Number of chunks created
        """
        try:
            # Update status to processing
            document.processing_status = 'processing'
            db.commit()
            
            # Parse document based on file type
            chunks = self._parse_document(document)
            
            # Classify and save chunks
            chunk_count = self._classify_and_save_chunks(db, document, chunks)
            
            # Update document with page count
            if chunks:
                document.page_count = max((c.page_number or 0) for c in chunks)
            
            # Update status to completed
            document.processing_status = 'completed'
            from datetime import datetime
            document.processed_at = datetime.utcnow()
            db.commit()
            
            return chunk_count
        
        except Exception as e:
            # Update status to failed
            document.processing_status = 'failed'
            db.commit()
            raise ValueError(f"Document processing failed: {str(e)}")
    
    def _parse_document(self, document: Document) -> List:
        """Parse document based on file type."""
        file_type = document.file_type.lower()
        
        if file_type == 'pdf':
            return self.pdf_parser.parse(document.file_path)
        elif file_type in ['docx', 'doc']:
            return self.docx_parser.parse(document.file_path)
        elif file_type in ['pptx', 'ppt']:
            return self.ppt_parser.parse(document.file_path)
        elif file_type in ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif']:
            return self.image_parser.parse(document.file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _classify_and_save_chunks(
        self,
        db: Session,
        document: Document,
        parsed_chunks: List
    ) -> int:
        """Classify parsed chunks and save to database."""
        chunk_count = 0
        
        for parsed_chunk in parsed_chunks:
            # Classify content
            content_type, confidence = self.classifier.classify_text(parsed_chunk.text)
            
            # Create database chunk
            db_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=parsed_chunk.chunk_index,
                raw_text=parsed_chunk.text,
                page_number=parsed_chunk.page_number,
                content_type=content_type,
                confidence_score=confidence,
                chunk_metadata=parsed_chunk.metadata
            )
            
            db.add(db_chunk)
            chunk_count += 1
        
        # Commit all chunks
        db.commit()
        
        return chunk_count

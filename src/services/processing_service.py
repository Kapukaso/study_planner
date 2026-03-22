"""Document processing service - orchestrates parsing and classification."""
from sqlalchemy.orm import Session
from typing import List
import logging

from src.models import Document, DocumentChunk
from src.parsers import PDFParser, DOCXParser, PPTParser, ImageParser
from src.parsers.exceptions import ParserError, CorruptedFileError, FileNotReadableError, UnsupportedFormatError
from src.classifier import ContentClassifier
from src.services.generation_service import ResourceGenerator

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Handles document parsing and content classification."""
    
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.docx_parser = DOCXParser()
        self.ppt_parser = PPTParser()
        self.image_parser = ImageParser()
        self.classifier = ContentClassifier()
    
    def process_document(self, db: Session, document: Document) -> dict:
        """
        Process document: parse, classify, save chunks, and generate resources.
        
        Args:
            db: Database session
            document: Document model to process
            
        Returns:
            Dictionary with processing results
        """
        try:
            # Update status to processing
            document.processing_status = 'processing'
            db.commit()
            
            # Parse document based on file type
            chunks = self._parse_document(document)
            
            if not chunks:
                logger.warning(f"No content extracted from document {document.id}")
                document.processing_status = 'completed'
                db.commit()
                return {"chunks": 0, "resources": {}}

            # Classify and save chunks
            chunk_count = self._classify_and_save_chunks(db, document, chunks)
            
            # Update document with page count
            document.page_count = max((c.page_number or 0) for c in chunks)
            
            # Generate study resources
            generator = ResourceGenerator(db)
            resource_results = generator.generate_resources_for_document(document.id)
            
            # Update status to completed
            document.processing_status = 'completed'
            from datetime import datetime
            document.processed_at = datetime.utcnow()
            db.commit()
            
            return {
                "chunks": chunk_count,
                "resources": resource_results
            }
        
        except (CorruptedFileError, FileNotReadableError, UnsupportedFormatError) as e:
            logger.error(f"Known error processing document {document.id}: {str(e)}")
            document.processing_status = 'failed'
            document.error_message = str(e)
            db.commit()
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error processing document {document.id}: {str(e)}")
            # Update status to failed
            document.processing_status = 'failed'
            document.error_message = f"Unexpected error: {str(e)}"
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
            raise UnsupportedFormatError(f"Unsupported file type: {file_type}")
    
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

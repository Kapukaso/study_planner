"""Image parser using Tesseract OCR."""
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
from PIL import Image
import pandas as pd

from src.parsers.base_parser import BaseParser, ParsedChunk

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageParser(BaseParser):
    """Parser for image files using OCR."""

    def __init__(self, chunk_size: int = 1000):
        self.tesseract_available = self._check_tesseract()
        self.chunk_size = chunk_size
        if not self.tesseract_available:
            logger.warning(
                "Tesseract is not available or not configured correctly. "
                "Image parsing will not be possible."
            )

    def _check_tesseract(self) -> bool:
        """Check if Tesseract is available."""
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            return True
        except ImportError:
            logger.error("pytesseract library not found. Please install it.")
            return False
        except Exception as e:
            logger.error(f"Tesseract is not installed or not in your PATH: {e}")
            return False

    def parse(self, file_path: str) -> List[ParsedChunk]:
        """
        Parse an image file using OCR, chunk the text, and return ParsedChunk objects.

        Args:
            file_path: Path to the image file.

        Returns:
            A list of ParsedChunk objects.
        """
        if not self.tesseract_available:
            raise EnvironmentError("Tesseract OCR is not available.")

        logger.info(f"Parsing image file: {file_path}")
        try:
            image = Image.open(file_path)
            full_text, avg_confidence = self._get_ocr_data(image)

            if not full_text.strip():
                logger.info("No text found in the image.")
                return []

            cleaned_text = self.clean_text(full_text)
            text_chunks = self.chunk_by_paragraphs(cleaned_text, self.chunk_size)

            parsed_chunks = []
            for i, text_chunk in enumerate(text_chunks):
                chunk = ParsedChunk(
                    text=text_chunk,
                    page_number=1,  # Images are single-page
                    chunk_index=i,
                    metadata=self._create_chunk_metadata(image, avg_confidence)
                )
                parsed_chunks.append(chunk)

            logger.info(f"Successfully parsed image and created {len(parsed_chunks)} chunks.")
            return parsed_chunks

        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error parsing image with OCR: {e}")
            raise ValueError(f"Failed to parse image {file_path}: {e}")

    def _get_ocr_data(self, image: Image.Image) -> Tuple[str, float]:
        """
        Extract text and calculate average confidence using pytesseract.

        Args:
            image: A PIL Image object.

        Returns:
            A tuple containing the full extracted text and the average confidence score.
        """
        import pytesseract
        
        # Use image_to_data to get detailed information including confidence scores
        data = pytesseract.image_to_data(
            image, output_type=pytesseract.Output.DATAFRAME
        )
        
        # Filter out entries with negative confidence (these are not words)
        data = data[data.conf != -1]
        
        # Calculate average confidence
        avg_confidence = data['conf'].mean() if not data.empty else 0.0
        
        # Reconstruct the text from the data
        full_text = " ".join(data['text'].dropna())
        
        return full_text, round(avg_confidence, 2)

    def _create_chunk_metadata(self, image: Image.Image, avg_confidence: float) -> Dict[str, Any]:
        """Create metadata dictionary for a parsed chunk."""
        return {
            'image_width': image.width,
            'image_height': image.height,
            'image_format': image.format,
            'image_mode': image.mode,
            'parser': 'tesseract-ocr',
            'ocr_confidence': avg_confidence,
        }

    def get_supported_formats(self) -> List[str]:
        """Get a list of supported image formats."""
        return ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif']

    def is_image_file(self, file_path: str) -> bool:
        """Check if a file is a supported image format."""
        ext = Path(file_path).suffix.lower().lstrip('.')
        return ext in self.get_supported_formats()
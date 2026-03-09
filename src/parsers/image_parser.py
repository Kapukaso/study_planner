"""Image parser using Tesseract OCR."""
import os
from pathlib import Path
from typing import List
from PIL import Image

from src.parsers.base_parser import BaseParser, ParsedChunk


class ImageParser(BaseParser):
    """Parser for image files using OCR."""

    def __init__(self):
        self.tesseract_available = self._check_tesseract()

    def _check_tesseract(self) -> bool:
        """Check if Tesseract is available."""
        try:
            import pytesseract
            # Try to get version to verify Tesseract binary is installed
            pytesseract.get_tesseract_version()
            return True
        except ImportError:
            return False
        except Exception:
            return False

    def parse(self, file_path: str) -> List[ParsedChunk]:
        """
        Parse image file using OCR.

        Args:
            file_path: Path to image file

        Returns:
            List of ParsedChunk objects
        """
        if not self.tesseract_available:
            raise ValueError("Tesseract OCR not available. Please install Tesseract and pytesseract.")

        try:
            import pytesseract

            # Open image
            image = Image.open(file_path)

            # Extract text using OCR
            text = pytesseract.image_to_string(image)

            if not text.strip():
                # No text found
                return []

            # Clean the text
            cleaned_text = self.clean_text(text)

            if not cleaned_text:
                return []

            # Create chunk
            chunk = ParsedChunk(
                text=cleaned_text,
                page_number=1,  # Images are treated as single "pages"
                chunk_index=0,
                metadata={
                    'image_width': image.width,
                    'image_height': image.height,
                    'image_format': image.format,
                    'image_mode': image.mode,
                    'parser': 'tesseract-ocr',
                    'ocr_confidence': self._get_confidence_score(text)
                }
            )

            return [chunk]

        except Exception as e:
            raise ValueError(f"Error parsing image with OCR: {str(e)}")

    def _get_confidence_score(self, text: str) -> float:
        """
        Get a rough confidence score based on text characteristics.
        This is a simple heuristic since pytesseract doesn't provide
        confidence scores in image_to_string by default.
        """
        if not text.strip():
            return 0.0

        # Simple heuristics for confidence
        word_count = len(text.split())
        char_count = len(text)

        # Very short text = low confidence
        if char_count < 10:
            return 0.2
        # Short text = medium confidence
        elif char_count < 50:
            return 0.5
        # Longer text = higher confidence
        else:
            return 0.8

    def get_supported_formats(self) -> List[str]:
        """Get list of supported image formats."""
        return ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif']

    def is_image_file(self, file_path: str) -> bool:
        """Check if file is a supported image format."""
        ext = Path(file_path).suffix.lower().lstrip('.')
        return ext in self.get_supported_formats()
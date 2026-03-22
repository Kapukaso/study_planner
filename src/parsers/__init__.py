"""Parsers package."""
from src.parsers.pdf_parser import PDFParser
from src.parsers.docx_parser import DOCXParser
from src.parsers.ppt_parser import PPTParser
from src.parsers.image_parser import ImageParser

__all__ = ["PDFParser", "DOCXParser", "PPTParser", "ImageParser"]

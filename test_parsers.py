"""Test document parsers."""
import os
import tempfile
from pathlib import Path

from src.parsers.pdf_parser import PDFParser
from src.parsers.docx_parser import DOCXParser
from src.parsers.ppt_parser import PPTParser


def test_pdf_parser():
    """Test PDF parser with basic functionality."""
    parser = PDFParser()

    # Create a simple test PDF
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            pdf_path = tmp.name

        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(50, 750, "Test PDF content for parsing.")
        c.drawString(50, 720, "This is a second line of text.")
        c.save()

        print("PDF Parser: Found {} chunks".format(len(chunks)))

        if chunks:
            print("First chunk text: {}...".format(chunks[0].text[:100]))
            print("Metadata: {}".format(chunks[0].metadata))

        # Test page count
        page_count = parser.get_page_count(pdf_path)
        print("PDF pages: {}".format(page_count))

        # Cleanup
        os.unlink(pdf_path)
        return True

    except ImportError:
        print("PDF Parser: reportlab not available, skipping PDF creation test")
        return True
    except Exception as e:
        print("PDF Parser test failed: {}".format(e))
        return False


def test_docx_parser():
    """Test DOCX parser with basic functionality."""
    parser = DOCXParser()

    try:
        from docx import Document

        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            docx_path = tmp.name

        # Create a simple DOCX
        doc = Document()
        doc.add_heading('Test Document', 0)
        doc.add_paragraph('This is a test paragraph with some content.')
        doc.add_paragraph('Another paragraph with different text.')

        # Add a simple table
        table = doc.add_table(rows=2, cols=2)
        table.cell(0, 0).text = 'Header 1'
        table.cell(0, 1).text = 'Header 2'
        table.cell(1, 0).text = 'Data 1'
        table.cell(1, 1).text = 'Data 2'

        doc.save(docx_path)

        print("DOCX Parser: Found {} chunks".format(len(chunks)))

        if chunks:
            print("First chunk text: {}...".format(chunks[0].text[:100]))
            print("Metadata: {}".format(chunks[0].metadata))

        # Test heading extraction
        headings = parser.extract_headings(docx_path)
        print("Headings found: {}".format(headings))

        # Cleanup
        os.unlink(docx_path)
        return True

    except ImportError:
        print("DOCX Parser: python-docx not available")
        return False
    except Exception as e:
        print("DOCX Parser test failed: {}".format(e))
        return False


def test_ppt_parser():
    """Test PPT parser with basic functionality."""
    parser = PPTParser()

    try:
        from pptx import Presentation

        with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as tmp:
            pptx_path = tmp.name

        # Create a simple PPTX
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        title = slide.shapes.title
        title.text = "Test Presentation"

        # Add content
        content = slide.placeholders[1]
        content.text = "This is slide content.\nSecond line of content."

        prs.save(pptx_path)

        print("PPT Parser: Found {} chunks".format(len(chunks)))

        if chunks:
            print("First chunk text: {}...".format(chunks[0].text[:100]))
            print("Metadata: {}".format(chunks[0].metadata))

        # Test slide count
        slide_count = parser.get_slide_count(pptx_path)
        print("PPT slides: {}".format(slide_count))

        # Cleanup
        os.unlink(pptx_path)
        return True

    except ImportError:
        print("PPT Parser: python-pptx not available")
        return False
    except Exception as e:
        print("PPT Parser test failed: {}".format(e))
        return False


if __name__ == "__main__":
    print("Testing Document Parsers")
    print("=" * 50)

    results = []

    print("\n1. Testing PDF Parser...")
    results.append(("PDF Parser", test_pdf_parser()))

    print("\n2. Testing DOCX Parser...")
    results.append(("DOCX Parser", test_docx_parser()))

    print("\n3. Testing PPT Parser...")
    results.append(("PPT Parser", test_ppt_parser()))

    print("\n" + "=" * 50)
    print("Test Results:")
    for name, success in results:
        status = "PASS" if success else "FAIL"
        print("{}: {}".format(name, status))

    passed = sum(1 for _, success in results if success)
    print("\nPassed: " + str(passed) + "/" + str(len(results)) + " tests")</content>
<parameter name="filePath">f:\Projects\studyPlanner\test_parsers.py
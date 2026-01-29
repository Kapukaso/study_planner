"""Test document processing - Demo script."""
import requests
import json
from pathlib import Path

# Base URL
BASE_URL = "http://127.0.0.1:8000"


def create_test_pdf():
    """Create a simple test PDF with sample content."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    filename = "test_study_notes.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Page 1: Definitions and Concepts
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Operating Systems - Study Notes")
    
    c.setFont("Helvetica", 12)
    y = 700
    
    # Definition
    c.drawString(50, y, "Process: A program in execution with its own address space and resources.")
    y -= 30
    
    # Concept
    c.drawString(50, y, "A process is the unit of work in modern operating systems. It consists of")
    y -= 15
    c.drawString(50, y, "program code, data, stack, and heap segments. The OS manages processes")
    y -= 15
    c.drawString(50, y, "through the Process Control Block (PCB) which contains process state and metadata.")
    y -= 40
    
    # Formula
    c.drawString(50, y, "CPU Utilization = 1 - p^n")
    y -= 15
    c.drawString(50, y, "where p = I/O wait time, n = number of processes")
    y -= 40
    
    # Question
    c.drawString(50, y, "Q1. Explain the four necessary conditions for deadlock. (10 marks)")
    y -= 15
    c.drawString(50, y, "     [May 2023]")
    y -= 40
    
    # Example
    c.drawString(50, y, "Example: Consider three processes P1, P2, P3 competing for resources R1, R2.")
    y -= 15
    c.drawString(50, y, "If P1 holds R1 and waits for R2, while P2 holds R2 and waits for R1,")
    y -= 15
    c.drawString(50, y, "a circular wait condition exists leading to deadlock.")
    y -= 40
    
    # Highlight
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Important: Always check for deadlock prevention before resource allocation!")
    
    c.save()
    return filename


def print_response(title: str, response):
    """Print formatted response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return data
    except:
        print(f"Response: {response.text}")
        return None


def test_document_processing():
    """Test complete document processing workflow."""
    print("\n" + "="*60)
    print("DOCUMENT PROCESSING - TEST")
    print("="*60)
    
    # Step 1: Create test subject
    print("\n[1] Creating test subject...")
    subject_response = requests.post(
        f"{BASE_URL}/api/subjects",
        json={
            "name": "Operating Systems",
            "code": "CS301",
            "priority": 9
        }
    )
    subject_data = print_response("Create Subject", subject_response)
    
    if not subject_data:
        print("\n[ERROR] Failed to create subject!")
        return
    
    subject_id = subject_data["id"]
    
    # Step 2: Create test PDF
    print("\n[2] Creating test PDF...")
    try:
        pdf_filename = create_test_pdf()
        print(f"Created test PDF: {pdf_filename}")
    except Exception as e:
        print(f"Skipping PDF creation (reportlab not installed): {e}")
        print("Please upload a PDF manually for testing")
        return
    
    # Step 3: Upload document
    print("\n[3] Uploading document...")
    with open(pdf_filename, 'rb') as f:
        upload_response = requests.post(
            f"{BASE_URL}/api/documents/upload",
            files={'file': (pdf_filename, f, 'application/pdf')},
            data={'subject_id': subject_id}
        )
    
    upload_data = print_response("Upload Document", upload_response)
    
    if not upload_data:
        print("\n[ERROR] Failed to upload document!")
        return
    
    document_id = upload_data["id"]
    
    # Step 4: Process document
    print("\n[4] Processing document (parsing + classification)...")
    process_response = requests.post(
        f"{BASE_URL}/api/documents/{document_id}/process"
    )
    process_data = print_response("Process Document", process_response)
    
    if not process_data:
        print("\n[ERROR] Failed to process document!")
        return
    
    # Step 5: Get chunk statistics
    print("\n[5] Getting chunk statistics...")
    stats_response = requests.get(
        f"{BASE_URL}/api/documents/{document_id}/chunks/stats"
    )
    stats_data = print_response("Chunk Statistics", stats_response)
    
    # Step 6: Get all chunks
    print("\n[6] Getting all chunks...")
    chunks_response = requests.get(
        f"{BASE_URL}/api/documents/{document_id}/chunks"
    )
    chunks_data = print_response("All Chunks", chunks_response)
    
    # Step 7: Filter by content type
    print("\n[7] Getting only formulas...")
    formula_response = requests.get(
        f"{BASE_URL}/api/documents/{document_id}/chunks?content_type=formula"
    )
    formula_data = print_response("Formula Chunks", formula_response)
    
    print("\n[8] Getting only questions...")
    pyq_response = requests.get(
        f"{BASE_URL}/api/documents/{document_id}/chunks?content_type=pyq"
    )
    pyq_data = print_response("PYQ Chunks", pyq_response)
    
    # Summary
    print("\n" + "="*60)
    print("[SUCCESS] Document Processing Complete!")
    print("="*60)
    print(f"\nSubject ID: {subject_id}")
    print(f"Document ID: {document_id}")
    
    if stats_data:
        print(f"\nTotal Chunks: {stats_data.get('total_chunks', 0)}")
        print(f"Average Confidence: {stats_data.get('avg_confidence', 0)}")
        print("\nChunks by Type:")
        for ctype, count in stats_data.get('by_type', {}).items():
            print(f"  - {ctype}: {count}")
    
    print(f"\nAPI Documentation: {BASE_URL}/docs")
    
    # Cleanup
    try:
        Path(pdf_filename).unlink()
        print(f"\nCleaned up test file: {pdf_filename}")
    except:
        pass


if __name__ == "__main__":
    try:
        test_document_processing()
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to server!")
        print(f"Make sure the server is running on {BASE_URL}")
        print("Run: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()

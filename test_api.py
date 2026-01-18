"""Test API endpoints - Demo script."""
import requests
import json
from datetime import date, timedelta

# Base URL
BASE_URL = "http://127.0.0.1:8000"

def print_response(title: str, response):
    """Print formatted response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")


def test_health():
    """Test health endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_create_subject():
    """Test creating a subject."""
    data = {
        "name": "Artificial Intelligence",
        "code": "CS401",
        "exam_date": str(date.today() + timedelta(days=45)),
        "priority": 9,
        "total_marks": 100
    }
    
    response = requests.post(f"{BASE_URL}/api/subjects", json=data)
    print_response("Create Subject", response)
    
    if response.status_code == 201:
        return response.json()["id"]
    return None


def test_list_subjects():
    """Test listing subjects."""
    response = requests.get(f"{BASE_URL}/api/subjects")
    print_response("List Subjects", response)
    return response.status_code == 200


def test_get_subject(subject_id: str):
    """Test getting a subject."""
    response = requests.get(f"{BASE_URL}/api/subjects/{subject_id}")
    print_response(f"Get Subject {subject_id}", response)
    return response.status_code == 200


def test_update_subject(subject_id: str):
    """Test updating a subject."""
    data = {
        "priority": 10,
        "total_marks": 150
    }
    
    response = requests.put(f"{BASE_URL}/api/subjects/{subject_id}", json=data)
    print_response(f"Update Subject {subject_id}", response)
    return response.status_code == 200


def test_upload_document(subject_id: str):
    """Test uploading a document (creates a dummy text file)."""
    # Create a dummy text file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pdf', delete=False) as f:
        f.write("This is a test PDF content for Study Planner")
        temp_path = f.name
    
    try:
        with open(temp_path, 'rb') as file:
            files = {'file': ('test_document.pdf', file, 'application/pdf')}
            data = {'subject_id': subject_id}
            
            response = requests.post(f"{BASE_URL}/api/documents/upload", files=files, data=data)
            print_response("Upload Document", response)
            
            if response.status_code == 201:
                return response.json()["id"]
    finally:
        import os
        os.unlink(temp_path)
    
    return None


def test_list_documents(subject_id: str):
    """Test listing documents."""
    response = requests.get(f"{BASE_URL}/api/documents", params={"subject_id": subject_id})
    print_response("List Documents", response)
    return response.status_code == 200


def run_all_tests():
    """Run all test cases."""
    print("\n" + "="*60)
    print("STUDY PLANNER API - TEST SUITE")
    print("="*60)
    
    # Test health
    if not test_health():
        print("\n[ERROR] Server health check failed!")
        return
    
    # Test subject creation
    subject_id = test_create_subject()
    if not subject_id:
        print("\n[ERROR] Failed to create subject!")
        return
    
    # Test list subjects
    test_list_subjects()
    
    # Test get specific subject
    test_get_subject(subject_id)
    
    # Test update subject
    test_update_subject(subject_id)
    
    # Test document upload
    document_id = test_upload_document(subject_id)
    if document_id:
        # Test list documents
        test_list_documents(subject_id)
    
    print("\n" + "="*60)
    print("[SUCCESS] All tests completed!")
    print("="*60)
    print(f"\nCreated Subject ID: {subject_id}")
    if document_id:
        print(f"Uploaded Document ID: {document_id}")
    print(f"\nAPI Documentation: {BASE_URL}/docs")
    print(f"Health Check: {BASE_URL}/health")


if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to server!")
        print(f"Make sure the server is running on {BASE_URL}")
        print("Run: uvicorn main:app --reload")

import pytest
from fastapi.testclient import TestClient
from app.main import app 

tables = ["departments", "jobs", "employees"]

client = TestClient(app)

def test_root():
    """Test if the root endpoint returns a success message."""
    response = client.get("/")
    assert response.status_code == 200

def test_upload_pdf_empty():
    """Test uploading an empty PDF file."""
    for table in tables:
        response = client.post(
            f"/upload/pdf/{table}/",  
            files={"file": ("empty.pdf", b"")}
        )
        assert response.status_code == 400

def test_upload_pdf_large_employees():
    """Test uploading a very large (1998 rows) PDF file."""
    file_path = "../data/hired.pdf"  

    with open(file_path, 'rb') as f:
        response = client.post(
            f"/upload/pdf/employees/",
            files={"file": ("hired.pdf", f, "application/pdf")}
        )
    assert response.status_code == 400

def test_upload_pdf_good_file_employees():
    """Test uploading a normal size (< 1000 rows) PDF file."""
    file_path = "../data/hired_p1.pdf"  

    with open(file_path, 'rb') as f:
        response = client.post(
            f"/upload/pdf/employees/",
            files={"file": ("hired_p1.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
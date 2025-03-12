import uuid  # Import uuid for generating unique identifiers
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app  # Ensure 'app' is correctly imported
from fastapi.testclient import TestClient

print(type(app))  # This should print <class 'fastapi.applications.FastAPI'>
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_create_patient(client):
    unique_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"  # Generate unique email
    response = client.post("/patients/", json={
        "name": "John Doe",
        "email": unique_email,
        "age": 30,
        "active": True
    })
    assert response.status_code == 200

def test_get_patient(client):
    unique_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    client.post("/patients/", json={
        "name": "John Doe",
        "email": unique_email,
        "age": 30,
        "active": True
    })
    
    response = client.get("/patients/1")  # Assuming the first inserted ID is 1
    assert response.status_code == 200

def test_delete_patient(client):
    unique_email = f"deleteuser_{uuid.uuid4().hex[:6]}@example.com"
    
    # ✅ First, create the patient
    create_response = client.post("/patients/", json={
        "name": "To Delete",
        "email": unique_email,
        "age": 35,
        "active": True
    })
    
    assert create_response.status_code == 200  # Ensure creation was successful
    
    # ✅ Get the patient ID from the response
    patient_id = create_response.json()["id"]

    # ✅ Now, delete the patient
    response = client.delete(f"/patients/{patient_id}")
    assert response.status_code == 200  # Expect successful deletion


def test_update_patient(client):
    patient_id = 1  # Ensure this patient exists before testing
    response = client.put(f"/patients/{patient_id}", json={
        "id": 1,
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "age": 32,
        "active": False
    })
    assert response.status_code == 200



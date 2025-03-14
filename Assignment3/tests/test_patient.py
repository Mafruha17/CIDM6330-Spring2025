import os
import sys
import uuid
import pytest
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app  # ✅ Ensure 'app' is correctly imported
client = TestClient(app)

# ✅ Clear all patients before running tests
client.delete("/patients/all")  # Ensure clean test data

def test_root(client: TestClient):  # Use fixture
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

def test_create_patient(client: TestClient):
    unique_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    response = client.post("/patients/", json={
        "name": "John Doe",
        "email": unique_email,
        "age": 30,
        "active": True
    })
    assert response.status_code == 200, response.json()

def test_get_patient(client: TestClient):
    unique_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    create_response = client.post("/patients/", json={
        "name": "John Doe",
        "email": unique_email,
        "age": 30,
        "active": True
    })
    assert create_response.status_code == 200, create_response.json()
    patient_id = create_response.json()["id"]

    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == 200, response.json()

def test_delete_patient(client: TestClient):
    unique_email = f"deleteuser_{uuid.uuid4().hex[:6]}@example.com"
    create_response = client.post("/patients/", json={
        "name": "To Delete",
        "email": unique_email,
        "age": 35,
        "active": True
    })
    assert create_response.status_code == 200, create_response.json()
    patient_id = create_response.json()["id"]

    response = client.delete(f"/patients/{patient_id}")
    assert response.status_code == 200, response.json()

def test_update_patient(client: TestClient):
    unique_email = f"updateuser_{uuid.uuid4().hex[:6]}@example.com"
    create_response = client.post("/patients/", json={
        "name": "Initial Name",
        "email": unique_email,
        "age": 40,
        "active": True
    })
    assert create_response.status_code == 200, create_response.json()
    patient_id = create_response.json()["id"]

    response = client.put(f"/patients/{patient_id}", json={
        "id": patient_id,
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "age": 32,
        "active": False
    })
    assert response.status_code == 200, response.json()

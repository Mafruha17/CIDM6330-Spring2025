import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import Session
from database.connection import get_db
from database.models import Patient
from schemas.patient import PatientSchema

# Utilize a test client
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_patient():
    response = client.post("/patients/", json={
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "active": True
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["age"] == 30
    assert data["active"] is True
    assert "id" in response.json()


def test_get_patient():
    patient_id = 1  # Use an existing patient ID
    response = client.get(f"/patients/{patient_id}")

    assert response.status_code == 200
    assert response.json()["id"] == patient_id


def test_get_all_patients():
    response = client.get("/patients/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_patient():
    patient_id = 1  # Ensure the patient exists first
    response = client.put(f"/patients/{patient_id}", json={
        "name": "Jane Doe",
        "age": 32
    })

    assert response.status_code == 200
    assert response.json()["name"] == "John Doe Updated"


def test_delete_patient():
    patient_id = 1  # Use a valid patient ID for deletion
    response = client.delete(f"/patients/{patient_id}")

    assert response.status_code == 200
    assert response.json() == {"message": "Patient deleted successfully"}

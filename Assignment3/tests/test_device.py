import os
import sys
import uuid
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app  # Ensure this points to your FastAPI app
client = TestClient(app)

def test_create_device(client: TestClient):
    patient_response = client.post("/patients/", json={
        "name": "Device Test Patient",
        "email": f"patient_{uuid.uuid4().hex[:6]}@example.com",
        "age": 30,
        "active": True
    })
    assert patient_response.status_code == 200, patient_response.json()
    patient_id = patient_response.json()["id"]

    unique_serial = str(uuid.uuid4())[:8]  # Generate a short unique serial number
    response = client.post("/devices/", json={
        "serial_number": unique_serial,
        "patient_id": patient_id,
        "active": True
    })
    assert response.status_code == 200, response.json()

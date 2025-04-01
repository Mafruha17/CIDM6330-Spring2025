import pytest
from rest_framework.test import APIClient
from mainapp.models import Patient, Device


@pytest.mark.django_db
def test_assign_and_unassign_device():
    client = APIClient()

    # Create a patient and device
    patient = Patient.objects.create(name="Alice", email="alice@example.com", age=30)
    device = Device.objects.create(serial_number="SN123", active=True)

    # Assign device to patient
    assign_url = f"/api/devices/{device.id}/assign/"
    response = client.post(assign_url, {"patient_id": patient.id}, format='json')
    assert response.status_code == 200
    assert response.data["patient"] == str(patient)

    # Unassign device
    unassign_url = f"/api/devices/{device.id}/unassign/"
    response = client.post(unassign_url, {}, format='json')
    assert response.status_code == 200
    assert response.data["patient"] is None

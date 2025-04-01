import pytest
from rest_framework.test import APIClient
from mainapp.models import Patient, Provider, PatientProvider


@pytest.mark.django_db
def test_assign_and_remove_provider():
    client = APIClient()

    # Create patient and provider
    patient = Patient.objects.create(name="Bob", email="bob@example.com", age=40)
    provider = Provider.objects.create(name="Dr. Smith", email="smith@clinic.com", specialty="Dermatology")

    # Assign provider
    assign_url = f"/api/patients/{patient.id}/assign_provider/"
    response = client.post(assign_url, {"provider_id": provider.id}, format='json')
    assert response.status_code == 200
    assert PatientProvider.objects.filter(patient=patient, provider=provider).exists()

    # Remove provider
    remove_url = f"/api/patients/{patient.id}/remove_provider/"
    response = client.post(remove_url, {"provider_id": provider.id}, format='json')
    assert response.status_code == 200
    assert not PatientProvider.objects.filter(patient=patient, provider=provider).exists()

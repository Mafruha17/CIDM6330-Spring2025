import pytest
from rest_framework.test import APIClient
from mainapp.models import Provider


@pytest.mark.django_db
def test_create_and_retrieve_provider():
    client = APIClient()

    # Create a provider
    provider_data = {
        "name": "Dr. Emily",
        "email": "emily@health.org",
        "specialty": "Cardiology"
    }

    create_response = client.post("/api/providers/", provider_data, format='json')
    assert create_response.status_code == 201
    created_provider_id = create_response.data["id"]

    # Retrieve the same provider
    retrieve_response = client.get(f"/api/providers/{created_provider_id}/")
    assert retrieve_response.status_code == 200
    assert retrieve_response.data["name"] == provider_data["name"]
    assert retrieve_response.data["email"] == provider_data["email"]
    assert retrieve_response.data["specialty"] == provider_data["specialty"]


@pytest.mark.django_db
def test_update_and_delete_provider():
    client = APIClient()

    # Create a provider
    provider = Provider.objects.create(name="Dr. Mike", email="mike@clinic.com", specialty="Neurology")

    # Update the provider
    update_data = {
        "name": "Dr. Mike Updated",
        "email": "mike@clinic.com",
        "specialty": "Neurosurgery"
    }
    update_response = client.put(f"/api/providers/{provider.id}/", update_data, format='json')
    assert update_response.status_code == 200
    assert update_response.data["specialty"] == "Neurosurgery"

    # Delete the provider
    delete_response = client.delete(f"/api/providers/{provider.id}/")
    assert delete_response.status_code == 204
    assert not Provider.objects.filter(id=provider.id).exists()

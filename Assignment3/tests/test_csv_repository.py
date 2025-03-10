import pytest
import os
from repositories.csv_repository import CSVRepository
from schemas.provider import ProviderSchema

# We'll store providers in this test CSV file
TEST_CSV_FILE = "test_providers.csv"

@pytest.fixture
def csv_repo():
    repo = CSVRepository(TEST_CSV_FILE)
    yield repo
    if os.path.exists(TEST_CSV_FILE):
        os.remove(TEST_CSV_FILE)

def test_create_provider(csv_repo):
    # Using "specialty" to match your ProviderSchema
    provider_data = ProviderSchema(name="Dr. John Doe", email="john@example.com", specialty="Cardiology")
    created_provider = csv_repo.create(provider_data)
    assert created_provider["id"] is not None
    assert created_provider["name"] == "Dr. John Doe"

def test_get_provider(csv_repo):
    provider_data = ProviderSchema(name="Dr. Jane Smith", email="jane@example.com", specialty="Neurology")
    created_provider = csv_repo.create(provider_data)
    fetched_provider = csv_repo.get(created_provider["id"])
    assert fetched_provider is not None
    assert fetched_provider["name"] == "Dr. Jane Smith"

def test_get_all_providers(csv_repo):
    # We know at least one provider has been created by earlier tests
    providers = csv_repo.get_all()
    assert len(providers) >= 1

def test_update_provider(csv_repo):
    provider_data = ProviderSchema(name="Dr. Alan Brown", email="alan@example.com", specialty="Pediatrics")
    created_provider = csv_repo.create(provider_data)
    update_data = ProviderSchema(name="Dr. Alan Updated")
    updated_provider = csv_repo.update(created_provider["id"], update_data)
    assert updated_provider is not None
    assert updated_provider["name"] == "Dr. Alan Updated"

def test_delete_provider(csv_repo):
    provider_data = ProviderSchema(name="Dr. Lisa Green", email="lisa@example.com", specialty="Dermatology")
    created_provider = csv_repo.create(provider_data)
    deleted = csv_repo.delete(created_provider["id"])
    assert deleted is True
    assert csv_repo.get(created_provider["id"]) is None

import pytest
from fastapi.testclient import TestClient
from main import app
from repositories.in_memory_repository import InMemoryRepository
from schemas.provider import ProviderSchema

# ✅ Set up test client
client = TestClient(app)

# ✅ Set up In-Memory Repository
@pytest.fixture
def in_memory_repo():
    return InMemoryRepository()

# ✅ Test Creating a Provider
def test_create_provider(in_memory_repo):
    provider_data = ProviderSchema(name="Dr. John Doe", email="john@example.com", specialization="Cardiology")
    created_provider = in_memory_repo.create(provider_data)
    assert created_provider["id"] is not None
    assert created_provider["name"] == "Dr. John Doe"

# ✅ Test Getting a Provider by ID
def test_get_provider(in_memory_repo):
    provider_data = ProviderSchema(name="Dr. Jane Smith", email="jane@example.com", specialization="Neurology")
    created_provider = in_memory_repo.create(provider_data)
    fetched_provider = in_memory_repo.get(created_provider["id"])
    assert fetched_provider is not None
    assert fetched_provider["name"] == "Dr. Jane Smith"

# ✅ Test Getting All Providers
def test_get_all_providers(in_memory_repo):
    providers = in_memory_repo.get_all()
    assert len(providers) > 0

# ✅ Test Updating a Provider
def test_update_provider(in_memory_repo):
    provider_data = ProviderSchema(name="Dr. Alan Brown", email="alan@example.com", specialization="Pediatrics")
    created_provider = in_memory_repo.create(provider_data.model_dump())  # ✅ Fixed model_dump()
    update_data = ProviderSchema(name="Dr. Alan Updated")
    updated_provider = in_memory_repo.update(created_provider["id"], update_data.model_dump(exclude_unset=True))  # ✅ Fixed model_dump()
    assert updated_provider is not None
    assert updated_provider["name"] == "Dr. Alan Updated"
    
# ✅ Test Deleting a Provider
def test_delete_provider(in_memory_repo):
    provider_data = ProviderSchema(name="Dr. Lisa Green", email="lisa@example.com", specialization="Dermatology")
    created_provider = in_memory_repo.create(provider_data)
    deleted = in_memory_repo.delete(created_provider["id"])
    assert deleted is True
    assert in_memory_repo.get(created_provider["id"]) is None

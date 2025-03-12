import uuid  # Add this to the imports
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from repositories.in_memory_repository import InMemoryRepository
from schemas.provider import ProviderSchema

@pytest.fixture
def in_memory_repo():
    return InMemoryRepository()

def test_create_provider(in_memory_repo):
    provider_data = ProviderSchema(name="Dr. John Doe", email="john@example.com", specialty="Cardiology")
    created_provider = in_memory_repo.create(provider_data)
    assert created_provider["id"] is not None
    assert created_provider["name"] == "Dr. John Doe"

def test_get_provider(in_memory_repo):
    provider_data = ProviderSchema(name="Dr. Jane Smith", email="jane@example.com", specialty="Neurology")
    created_provider = in_memory_repo.create(provider_data)
    fetched_provider = in_memory_repo.get(created_provider["id"])

    assert fetched_provider is not None
    assert fetched_provider["name"] == "Dr. Jane Smith"

import uuid  # Ensure uuid is imported

def test_get_all_providers(in_memory_repo):
    # ✅ Create at least one provider first
    in_memory_repo.create({
        "name": "Dr. Smith",
        "email": f"drsmith_{uuid.uuid4().hex[:6]}@example.com",
        "specialty": "Cardiology"
    })

    providers = in_memory_repo.get_all()
    
    # ✅ Now, there should be at least one provider
    assert len(providers) >= 1


def test_update_provider(in_memory_repo):
    provider_data = ProviderSchema(name="Dr. Alan Brown", email="alan@example.com", specialty="Pediatrics")
    created_provider = in_memory_repo.create(provider_data)

    update_data = ProviderSchema(name="Dr. Alan Updated", email="alan@example.com", specialty="Pediatrics")
    updated_provider = in_memory_repo.update(created_provider["id"], update_data)

    assert updated_provider is not None
    assert updated_provider["name"] == "Dr. Alan Updated"


def test_delete_provider(in_memory_repo):
    provider_data = ProviderSchema(name="Dr. Lisa Green", email="lisa@example.com", specialty="Dermatology")
    created_provider = in_memory_repo.create(provider_data)
    
    deleted = in_memory_repo.delete(created_provider["id"])
    
    assert deleted is True
    assert in_memory_repo.get(created_provider["id"]) is None

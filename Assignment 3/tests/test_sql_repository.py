import pytest
from sqlmodel import Session, SQLModel, create_engine
from database.models import Provider
from repositories.sql_repository import SQLRepository
from schemas.provider import ProviderSchema

# Create a test database
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)

@pytest.fixture
def db_session():
    with Session(engine) as session:
        yield session

@pytest.fixture
def provider_repo(db_session):
    return SQLRepository(db_session, Provider)

# ✅ Test Creating a Provider
def test_create_provider(provider_repo):
    provider_data = ProviderSchema(name="Dr. John Doe", email="john@example.com", specialization="Cardiology")
    created_provider = provider_repo.create(provider_data)
    assert created_provider.id is not None
    assert created_provider.name == "Dr. John Doe"

# ✅ Test Getting a Provider by ID
def test_get_provider(provider_repo):
    provider_data = ProviderSchema(name="Dr. Jane Smith", email="jane@example.com", specialization="Neurology")
    created_provider = provider_repo.create(provider_data)
    fetched_provider = provider_repo.get(created_provider.id)
    assert fetched_provider is not None
    assert fetched_provider.name == "Dr. Jane Smith"

# ✅ Test Getting All Providers
def test_get_all_providers(provider_repo):
    providers = provider_repo.get_all()
    assert len(providers) > 0

# ✅ Test Updating a Provider
def test_update_provider(provider_repo):
    provider_data = ProviderSchema(name="Dr. Alan Brown", email="alan@example.com", specialization="Pediatrics")
    created_provider = provider_repo.create(provider_data)
    update_data = ProviderSchema(name="Dr. Alan Updated")
    updated_provider = provider_repo.update(created_provider.id, update_data)
    assert updated_provider is not None
    assert updated_provider.name == "Dr. Alan Updated"

# ✅ Test Deleting a Provider
def test_delete_provider(provider_repo):
    provider_data = ProviderSchema(name="Dr. Lisa Green", email="lisa@example.com", specialization="Dermatology")
    created_provider = provider_repo.create(provider_data)
    deleted = provider_repo.delete(created_provider.id)
    assert deleted is True
    assert provider_repo.get(created_provider.id) is None

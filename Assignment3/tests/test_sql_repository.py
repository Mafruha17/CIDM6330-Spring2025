import pytest
from sqlmodel import create_engine, Session, SQLModel
from database.models import Provider
from repositories.provider_repository import ProviderRepository
from schemas.provider import ProviderSchema

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

@pytest.fixture
def db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def provider_repo(db):
    return ProviderRepository(db)

def test_create_provider(db):
    provider_repo = ProviderRepository(db)
    provider_data = ProviderSchema(name="Dr. John Doe", email="john@example.com", specialty="Cardiology")
    created_provider = provider_repo.create(provider_data)
    assert created_provider.id is not None
    assert created_provider.name == "Dr. John Doe"

def test_get_provider(db: Session):
    provider_repo = ProviderRepository(db)
    provider_data = ProviderSchema(name="Dr. Jane Smith", email="jane@example.com", specialty="Cardiology")
    created_provider = provider_repo.create(provider_data)
    fetched_provider = provider_repo.get(created_provider.id)
    assert fetched_provider.name == created_provider.name

def test_get_all_providers(db: Session):
    provider_repo = ProviderRepository(db)
    provider_repo.create(ProviderSchema(name="Dr. Alan Brown", email="alan@example.com", specialty="Pediatrics"))
    providers = provider_repo.get_all()
    assert len(providers) > 0

def test_update_provider(db: Session):
    provider_repo = ProviderRepository(db)
    created_provider = provider_repo.create(ProviderSchema(name="Dr. Lisa Green", email="lisa@example.com", specialty="Dermatology"))
    updated_provider = provider_repo.update(created_provider.id, ProviderSchema(name="Dr. Lisa Green"))
    assert updated_provider.name == "Dr. Lisa Green"

def test_delete_provider(db: Session):
    provider_repo = ProviderRepository(db)
    created_provider = provider_repo.create(ProviderSchema(name="Dr. Lisa Green", email="lisa@example.com", specialty="Dermatology"))
    deleted = provider_repo.delete(created_provider.id)
    assert deleted is True
    assert provider_repo.get(created_provider.id) is None

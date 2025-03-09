from sqlmodel import Session
from database.models import Provider
from schemas.provider import ProviderSchema
from repositories.provider_repository import ProviderRepository
from typing import Optional, List

def create_provider(db: Session, provider_data: ProviderSchema) -> Provider:
    return ProviderRepository(db).create(provider_data.model_dump())

def get_provider(db: Session, provider_id: int) -> Optional[Provider]:
    return ProviderRepository(db).get(provider_id)

def get_all_providers(db: Session) -> List[Provider]:
    return ProviderRepository(db).get_all()

def update_provider(db: Session, provider_id: int, provider_data: ProviderSchema) -> Optional[Provider]:
    return ProviderRepository(db).update(provider_id, provider_data.model_dump(exclude_unset=True))

def delete_provider(db: Session, provider_id: int) -> bool:
    return ProviderRepository(db).delete(provider_id)

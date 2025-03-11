from sqlmodel import Session, select
from typing import Optional, List
from fastapi import HTTPException
from database.models import Provider, Patient
from repositories.provider_repository import ProviderRepository
from schemas.provider import ProviderSchema


def create_provider(db: Session, provider_data: ProviderSchema) -> Provider:
    return ProviderRepository(db).create(provider_data.dict())


def get_provider(db: Session, provider_id: int) -> Optional[Provider]:
    provider = ProviderRepository(db).get_by_id(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


def get_all_providers(db: Session) -> List[Provider]:
    return ProviderRepository(db).get_all()


def update_provider(db: Session, provider_id: int, provider_data: ProviderSchema) -> Optional[Provider]:
    updated_provider = ProviderRepository(db).update(provider_id, provider_data)
    if not updated_provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return updated_provider


def delete_provider(db: Session, provider_id: int) -> dict:
    success = ProviderRepository(db).delete(provider_id)
    if not success:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Provider deleted successfully"}

def get_patients_by_provider(db: Session, provider_id: int) -> List[Patient]:
    statement = select(Patient).join(Patient.providers).where(Provider.id == provider_id)
    results = db.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail="No patients found for this provider")
    return results

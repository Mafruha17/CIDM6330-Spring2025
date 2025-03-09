from fastapi import HTTPException
from sqlmodel import Session, select
from typing import Optional, List

from database.models import Patient, Device, Provider
from schemas.patient import PatientSchema
from schemas.device import DeviceSchema
from schemas.provider import ProviderSchema

from repositories.patient_repository import PatientRepository
from repositories.device_repository import DeviceRepository
from repositories.provider_repository import ProviderRepository


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

def get_patients_by_provider(db: Session, provider_id: int):
    statement = select(Patient).where(Patient.provider_id == provider_id)
    results = db.exec(statement)
    return results.all()


from sqlalchemy.orm import Session
from database.models import Patient, Device, Provider
from schemas.patient import PatientSchema
from schemas.device import DeviceSchema
from schemas.provider import ProviderSchema
from repositories.patient_repository import PatientRepository
from repositories.device_repository import DeviceRepository
from repositories.provider_repository import ProviderRepository
from typing import Optional, List

################
## Patient CRUD
################

def create_patient(db: Session, patient_data: PatientSchema) -> Patient:
    return PatientRepository(db).create(patient_data)

def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return PatientRepository(db).get(patient_id)

def get_all_patients(db: Session) -> List[Patient]:
    return PatientRepository(db).get_all()

def update_patient(db: Session, patient_id: int, patient_data: PatientSchema) -> Optional[Patient]:
    return PatientRepository(db).update(patient_id, patient_data)

def delete_patient(db: Session, patient_id: int) -> bool:
    return PatientRepository(db).delete(patient_id)

################
## Device CRUD
################

def create_device(db: Session, device_data: DeviceSchema) -> Device:
    return DeviceRepository(db).create(device_data)

def get_device(db: Session, device_id: int) -> Optional[Device]:
    return DeviceRepository(db).get(device_id)

def get_all_devices(db: Session) -> List[Device]:
    return DeviceRepository(db).get_all()

def update_device(db: Session, device_id: int, device_data: DeviceSchema) -> Optional[Device]:
    return DeviceRepository(db).update(device_id, device_data)

def delete_device(db: Session, device_id: int) -> bool:
    return DeviceRepository(db).delete(device_id)

################
## Provider CRUD
################
def create_provider(db: Session, provider_data: ProviderSchema) -> Provider:
    return ProviderRepository(db).create(provider_data)

def get_provider(db: Session, provider_id: int) -> Optional[Provider]:
    return ProviderRepository(db).get(provider_id)

def get_all_providers(db: Session) -> List[Provider]:
    return ProviderRepository(db).get_all()

def update_provider(db: Session, provider_id: int, provider_data: ProviderSchema) -> Optional[Provider]:
    return ProviderRepository(db).update(provider_id, provider_data)

def delete_provider(db: Session, provider_id: int) -> bool:
    return ProviderRepository(db).delete(provider_id)

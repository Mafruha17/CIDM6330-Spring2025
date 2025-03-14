from sqlmodel import Session
from schemas.patient import PatientSchema
from repositories.patient_repository import PatientRepository
from repositories.provider_repository import ProviderRepository
from repositories.device_repository import DeviceRepository
from typing import Optional, List
from database.models import Patient, Provider

def create_patient(db: Session, patient_data: PatientSchema) -> Patient: 
    return PatientRepository(db).create(patient_data)

def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return PatientRepository(db).get(patient_id)

def get_all_patients(db: Session) -> list[Patient]:
    return PatientRepository(db).get_all()

def update_patient(db: Session, patient_id: int, patient_data: PatientSchema) -> Optional[Patient]:
    return PatientRepository(db).update(patient_id, patient_data)

def delete_patient(db: Session, patient_id: int) -> bool:
    return PatientRepository(db).delete(patient_id)

def assign_provider_to_patient(db: Session, patient_id: int, provider_id: int) -> Optional[Patient]:
    patient_repo = PatientRepository(db)
    provider_repo = ProviderRepository(db)
    patient = patient_repo.get(patient_id)
    provider = provider_repo.get(provider_id)
    
    if not patient or not provider:
        return None

    if provider in patient.providers:
        return patient
    
    patient.providers.append(provider)
    db.commit()
    db.refresh(patient)
    return patient

def remove_provider_from_patient(db: Session, patient_id: int, provider_id: int) -> Optional[Patient]:
    patient_repo = PatientRepository(db)
    provider_repo = ProviderRepository(db)
    patient = patient_repo.get(patient_id)
    provider = provider_repo.get(provider_id)

    if not patient or not provider:
        return None

    if provider in patient.providers:
        patient.providers.remove(provider)
        db.commit()
        db.refresh(patient)

    return patient
# ✅ Remove a device from a patient (One-to-Many)
def remove_device_from_patient(db: Session, patient_id: int, device_id: int) -> Optional[Patient]:
    patient_repo = PatientRepository(db)
    devise_repo = DeviceRepository(db)
    patient = patient_repo.get(patient_id)
    device = devise_repo.get(device_id)   
    if not patient or not device:
        return None  # Either patient or device does not exist
    if device in patient.devices:
        patient.devices.remove(device)  # Remove device from patient
        db.commit()
    return patient

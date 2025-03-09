from fastapi import HTTPException
from sqlmodel import Session
from database.models import Patient, Device, Provider
from schemas.patient import PatientSchema
from schemas.device import DeviceSchema
from schemas.provider import ProviderSchema
from repositories.patient_repository import PatientRepository
from repositories.device_repository import DeviceRepository
from repositories.provider_repository import ProviderRepository
from typing import Optional, List

def create_patient(db: Session, patient_data: PatientSchema) -> Patient:
    return PatientRepository(db).create(patient_data.model_dump())

def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return PatientRepository(db).get(patient_id)

def get_all_patients(db: Session) -> List[Patient]:
    return PatientRepository(db).get_all()

def assign_provider_to_patient(db: Session, patient_id: int, provider_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    
    if not patient or not provider:
        return None
    
    if provider in patient.providers:
        return patient  # Already assigned
    
    patient.providers.append(provider)
    db.commit()
    return patient

def assign_device_to_patient(db: Session, patient_id: int, device_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    device = db.query(Device).filter(Device.id == device_id).first()

    if not patient or not device:
        return None  # Either patient or device does not exist

    if device in patient.devices:
        return patient  # Already assigned

    patient.devices.append(device)  # Assign device to patient
    db.commit()
    return patient

def update_patient(db: Session, patient_id: int, patient_data: PatientSchema):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        return None  # Patient not found

    patient_dict = patient_data.model_dump(exclude_unset=True, exclude={"device_ids", "provider_ids"})
    for key, value in patient_dict.items():
        setattr(patient, key, value)

    if "device_ids" in patient_data.model_dump():
        new_devices = db.query(Device).filter(Device.id.in_(patient_data.device_ids)).all()
        patient.devices = new_devices

    if "provider_ids" in patient_data.model_dump():
        new_providers = db.query(Provider).filter(Provider.id.in_(patient_data.provider_ids)).all()
        patient.providers = new_providers

    db.commit()
    db.refresh(patient)
    return patient

def remove_provider_from_patient(db: Session, patient_id: int, provider_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not patient or not provider:
        return None

    if provider in patient.providers:
        patient.providers.remove(provider)
        db.commit()
    
    return patient

def remove_device_from_patient(db: Session, patient_id: int, device_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    device = db.query(Device).filter(Device.id == device_id).first()

    if not patient or not device:
        return None  # Either patient or device does not exist

    if device in patient.devices:
        patient.devices.remove(device)
        db.commit()

    return patient

def delete_patient(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient.providers = []
    patient.devices = []
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

def create_device(db: Session, device_data: DeviceSchema) -> Device:
    return DeviceRepository(db).create(device_data.model_dump())

def get_device(db: Session, device_id: int) -> Optional[Device]:
    return DeviceRepository(db).get(device_id)

def get_all_devices(db: Session) -> List[Device]:
    return DeviceRepository(db).get_all()

def update_device(db: Session, device_id: int, device_data: DeviceSchema) -> Optional[Device]:
    return DeviceRepository(db).update(device_id, device_data.model_dump(exclude_unset=True))

def delete_device(db: Session, device_id: int) -> bool:
    return DeviceRepository(db).delete(device_id)

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

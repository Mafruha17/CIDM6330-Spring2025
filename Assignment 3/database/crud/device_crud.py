from fastapi import HTTPException
from sqlmodel import Session, select
from typing import Optional, List

from database.models import Device, Patient, Provider
from schemas.patient import PatientSchema
from schemas.device import DeviceSchema
from schemas.provider import ProviderSchema

from repositories.patient_repository import PatientRepository
from repositories.device_repository import DeviceRepository
from repositories.provider_repository import ProviderRepository


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


def assign_device_to_patient(db: Session, patient_id: int, device_id: int):
    patient = db.get(Patient, patient_id)
    device = db.get(Device, device_id)

    if not patient or not device:
        return None  # Either patient or device does not exist

    if device in patient.devices:
        return patient  # Already assigned

    patient.devices.append(device)  # Assign device to patient
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

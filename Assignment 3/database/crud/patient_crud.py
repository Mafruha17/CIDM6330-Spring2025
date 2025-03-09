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

# ✅ Create a new Patient
def create_patient(db: Session, patient_data: PatientSchema) -> Patient:
    return PatientRepository(db).create(patient_data)

# ✅ Get a Patient by ID
def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return PatientRepository(db).get(patient_id)

# ✅ Get all Patients
def get_all_patients(db: Session) -> List[Patient]:
    return PatientRepository(db).get_all()

# ✅ Assign a Provider to a Patient (Many-to-Many)
def assign_provider_to_patient(db: Session, patient_id: int, provider_id: int):
    statement = select(Patient).where(Patient.id == patient_id)
    patient = db.exec(statement).first()

    statement = select(Provider).where(Provider.id == provider_id)
    provider = db.exec(statement).first()

    if not patient or not provider:
        return None  # Patient or Provider not found

    if provider in patient.providers:
        return patient  # Already assigned

    patient.providers.append(provider)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

# ✅ Assign a Device to a Patient (One-to-Many)
def assign_device_to_patient(db: Session, patient_id: int, device_id: int):
    statement = select(Patient).where(Patient.id == patient_id)
    patient = db.exec(statement).first()

    statement = select(Device).where(Device.id == device_id)
    device = db.exec(statement).first()

    if not patient or not device:
        return None  # Either patient or device does not exist

    if device in patient.devices:
        return patient  # Already assigned

    patient.devices.append(device)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

# ✅ Update a Patient
def update_patient(db: Session, patient_id: int, patient_data: PatientSchema):
    statement = select(Patient).where(Patient.id == patient_id)
    patient = db.exec(statement).first()

    if not patient:
        return None  # Patient not found

    patient_dict = patient_data.model_dump(exclude_unset=True, exclude={"device_ids", "provider_ids"})
    for key, value in patient_dict.items():
        setattr(patient, key, value)

    if "device_ids" in patient_data.model_dump():
        statement = select(Device).where(Device.id.in_(patient_data.device_ids))
        new_devices = db.exec(statement).all()
        patient.devices = new_devices

    if "provider_ids" in patient_data.model_dump():
        statement = select(Provider).where(Provider.id.in_(patient_data.provider_ids))
        new_providers = db.exec(statement).all()
        patient.providers = new_providers

    db.commit()
    db.refresh(patient)
    return patient

# ✅ Remove a Provider from a Patient
def remove_provider_from_patient(db: Session, patient_id: int, provider_id: int):
    statement = select(Patient).where(Patient.id == patient_id)
    patient = db.exec(statement).first()

    statement = select(Provider).where(Provider.id == provider_id)
    provider = db.exec(statement).first()

    if not patient or not provider:
        return None  # Not found

    if provider in patient.providers:
        patient.providers.remove(provider)
        db.commit()

    return patient

# ✅ Remove a Device from a Patient
def remove_device_from_patient(db: Session, patient_id: int, device_id: int):
    statement = select(Patient).where(Patient.id == patient_id)
    patient = db.exec(statement).first()

    statement = select(Device).where(Device.id == device_id)
    device = db.exec(statement).first()

    if not patient or not device:
        return None  # Not found

    if device in patient.devices:
        patient.devices.remove(device)
        db.commit()

    return patient

# ✅ Delete a Patient
def delete_patient(db: Session, patient_id: int):
    statement = select(Patient).where(Patient.id == patient_id)
    patient = db.exec(statement).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient.providers = []
    patient.devices = []
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

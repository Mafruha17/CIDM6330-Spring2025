from fastapi import HTTPException
from sqlmodel import Session, select
from database.models import Patient, Provider
from schemas.patient import PatientSchema
from repositories.patient_repository import PatientRepository
from typing import Optional, List

def create_patient(db: Session, patient_data: PatientSchema) -> Patient:
    return PatientRepository(db).create(patient_data.model_dump())

def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return PatientRepository(db).get(patient_id)

def get_all_patients(db: Session) -> List[Patient]:
    return PatientRepository(db).get_all()

def update_patient(db: Session, patient_id: int, patient_data: PatientSchema):
    # For demonstration, we manually update. You could also do:
    #   PatientRepository(db).update(patient_id, patient_data.model_dump(...))
    patient = db.exec(select(Patient).where(Patient.id == patient_id)).first()
    if not patient:
        return None

    patient_dict = patient_data.model_dump(exclude_unset=True, exclude={"device_ids", "provider_ids"})
    for key, value in patient_dict.items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)
    return patient

def delete_patient(db: Session, patient_id: int):
    patient = db.exec(select(Patient).where(Patient.id == patient_id)).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

def assign_provider_to_patient(db: Session, patient_id: int, provider_id: int):
    patient = db.exec(select(Patient).where(Patient.id == patient_id)).first()
    provider = db.exec(select(Provider).where(Provider.id == provider_id)).first()

    if not patient or not provider:
        return None

    if provider in patient.providers:
        return patient  # Already assigned

    patient.providers.append(provider)
    db.commit()
    return patient

def remove_provider_from_patient(db: Session, patient_id: int, provider_id: int):
    patient = db.exec(select(Patient).where(Patient.id == patient_id)).first()
    provider = db.exec(select(Provider).where(Provider.id == provider_id)).first()

    if not patient or not provider:
        return None

    if provider in patient.providers:
        patient.providers.remove(provider)
        db.commit()

    return patient

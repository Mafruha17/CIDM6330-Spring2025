from fastapi import HTTPException
from sqlmodel import Session
from database.models import Patient, Device, Provider
from schemas.patient import PatientSchema
from repositories.patient_repository import PatientRepository
from typing import Optional, List

def create_patient(db: Session, patient_data: PatientSchema) -> Patient:
    return PatientRepository(db).create(patient_data.model_dump())

def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return PatientRepository(db).get(patient_id)

def update_patient(db: Session, patient_id: int, patient_data: PatientSchema):
    patient = db.get(Patient, patient_id)
    if not patient:
        return None

    patient_dict = patient_data.model_dump(exclude_unset=True, exclude={"device_ids", "provider_ids"})
    for key, value in patient_dict.items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)
    return patient

def delete_patient(db: Session, patient_id: int):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

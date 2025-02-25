from sqlalchemy.orm import Session
from database.models import Patient, Device
from schemas.patient import PatientSchema
from fastapi import HTTPException

# Create a new patient
def create_patient(db: Session, patient_data: dict):
    new_patient = Patient(**patient_data)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return PatientSchema.model_validate(new_patient)

# Get patient by ID
def get_patient(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return PatientSchema.model_validate(patient)

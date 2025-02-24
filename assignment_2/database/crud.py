from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models.patient import Patient
from schemas.patient import PatientSchema  # ✅ Ensure this is a Pydantic schema

def create_patient(db: Session, patient_data: dict):
    try:
        new_patient = Patient(**patient_data)
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        return PatientSchema.model_validate(new_patient)  # ✅ Convert SQLAlchemy → Pydantic
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Patient with this email already exists.")

def get_patient(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")
    return PatientSchema.model_validate(patient)  # ✅ Convert SQLAlchemy → Pydantic

def update_patient(db: Session, patient_id: int, updated_data: dict):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")
    
    try:
        for key, value in updated_data.items():
            setattr(patient, key, value)
        db.commit()
        db.refresh(patient)
        return PatientSchema.model_validate(patient)  # ✅ Convert SQLAlchemy → Pydantic
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating patient.")

def delete_patient(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")
    
    db.delete(patient)
    db.commit()
    return {"message": f"Patient {patient_id} deleted successfully."}

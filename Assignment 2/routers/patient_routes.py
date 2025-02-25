from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.crud import create_patient, get_patient
from schemas.patient import PatientSchema

router = APIRouter()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/patients/", response_model=PatientSchema)
def create(patient: PatientSchema, db: Session = Depends(get_db)):
    return create_patient(db, patient.model_dump())

@router.get("/patients/{patient_id}", response_model=PatientSchema)
def read(patient_id: int, db: Session = Depends(get_db)):
    return get_patient(db, patient_id)

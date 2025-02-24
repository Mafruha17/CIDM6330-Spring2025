from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.crud import create_patient, get_patient, update_patient, delete_patient
from schemas.patient import PatientSchema, PatientCreate  # ✅ Import both schemas

router = APIRouter()

@router.post("/patients/", response_model=PatientSchema)  # ✅ Fix: Use correct schema
def create(patient: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db, patient.model_dump())  # ✅ Ensure input is dict

@router.get("/patients/{patient_id}", response_model=PatientSchema)  # ✅ Fix response model
def read(patient_id: int, db: Session = Depends(get_db)):
    return get_patient(db, patient_id)

@router.put("/patients/{patient_id}", response_model=PatientSchema)  # ✅ Fix response model
def update(patient_id: int, patient: PatientCreate, db: Session = Depends(get_db)):
    return update_patient(db, patient_id, patient.model_dump())  # ✅ Ensure dict

@router.delete("/patients/{patient_id}")  # ✅ No need for a response model here
def delete(patient_id: int, db: Session = Depends(get_db)):
    return delete_patient(db, patient_id)

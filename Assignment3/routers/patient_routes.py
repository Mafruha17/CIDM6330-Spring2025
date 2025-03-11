from fastapi import APIRouter, Depends, HTTPException
from schemas.patient import PatientSchema
from database.connection import get_db
from database.models import Patient
from typing import Optional, List
from sqlmodel import Session
from database.crud.patient_crud import (
    create_patient, get_patient, get_all_patients, update_patient, delete_patient
)

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/", response_model=List[Patient])
def read_patients(db: Session = Depends(get_db)):
    return get_all_patients(db)

@router.post("/", response_model=Patient)
def create_patient_route(patient: PatientSchema, db: Session = Depends(get_db)):
    return create_patient(db, patient)

@router.get("/{patient_id}", response_model=Optional[Patient])
def get_patient_route(patient_id: int, db: Session = Depends(get_db)):
    return get_patient(db, patient_id)

@router.put("/{patient_id}", response_model=Optional[Patient])
def update_patient_route(patient_id: int, patient_data: PatientSchema, db: Session = Depends(get_db)):
    return update_patient(db, patient_id, patient_data)

@router.delete("/{patient_id}")
def delete_patient_route(patient_id: int, db: Session = Depends(get_db)):
    success = delete_patient(db, patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Deleted"}

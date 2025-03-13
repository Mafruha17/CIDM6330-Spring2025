from fastapi import APIRouter, Depends, HTTPException
from schemas.patient import PatientSchema
from database.connection import get_db
from typing import List, Optional
from sqlmodel import Session
import traceback  # Import traceback to log errors

from database.crud.patient_crud import (
    create_patient, get_patient, get_all_patients, update_patient, delete_patient
)

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/", response_model=List[PatientSchema], summary="Retrieve all patients")
def read_patients(db: Session = Depends(get_db)):
    """Fetch all patients from the database."""
    try:
        print("✅ DEBUG: Entered GET /patients/ route")  # Debug message
        patients = get_all_patients(db)
        print(f"✅ DEBUG: Retrieved {len(patients)} patients.")  # Log count
        return patients
    except Exception as e:
        print("❌ ERROR in `GET /patients/`")  # Debug error
        traceback.print_exc()  # Print full error details in logs
        raise HTTPException(status_code=500, detail=str(e))  # Show error in response

@router.post("/", response_model=PatientSchema, summary="Create a new patient")
def create_patient_route(patient: PatientSchema, db: Session = Depends(get_db)):
    """Create a new patient in the database."""
    try:
        new_patient = create_patient(db, patient)
        return new_patient
    except Exception as e:
        print("❌ ERROR in `POST /patients/`")  # Debug error
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{patient_id}", response_model=PatientSchema, summary="Retrieve a patient by ID")
def get_patient_route(patient_id: int, db: Session = Depends(get_db)):
    """Fetch a single patient by ID."""
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{patient_id}", response_model=PatientSchema, summary="Update an existing patient")
def update_patient_route(patient_id: int, patient_data: PatientSchema, db: Session = Depends(get_db)):
    """Update patient details."""
    updated_patient = update_patient(db, patient_id, patient_data)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient

@router.delete("/{patient_id}", summary="Delete a patient")
def delete_patient_route(patient_id: int, db: Session = Depends(get_db)):
    """Delete a patient from the database."""
    success = delete_patient(db, patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Deleted"}

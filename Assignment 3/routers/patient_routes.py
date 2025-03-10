from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from database.connection import get_db
from schemas.patient import PatientSchema
from database.crud.patient_crud import (
    create_patient, get_patient, get_all_patients, update_patient, delete_patient,
    assign_provider_to_patient, remove_provider_from_patient
)

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/", response_model=PatientSchema, summary="Create a new patient")
def create_patient_route(patient: PatientSchema, db: Session = Depends(get_db)):
    return create_patient(db, patient)


@router.get("/{patient_id}", response_model=PatientSchema, summary="Get a patient by ID")
def get_patient_route(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get("/", response_model=List[PatientSchema], summary="Get all patients")
def get_all_patients_route(db: Session = Depends(get_db)):
    return get_all_patients(db)


@router.put("/{patient_id}", response_model=PatientSchema, summary="Update a patient")
def update_patient_route(patient_id: int, patient_data: PatientSchema, db: Session = Depends(get_db)):
    updated_patient = update_patient(db, patient_id, patient_data)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient


@router.delete("/{patient_id}", summary="Delete a patient")
def delete_patient_route(patient_id: int, db: Session = Depends(get_db)):
    if not delete_patient(db, patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}

@router.post("/{patient_id}/assign-provider/{provider_id}", summary="Assign provider to patient")
def assign_provider_to_patient_route(patient_id: int, provider_id: int, db: Session = Depends(get_db)):
    assigned_patient = assign_provider_to_patient(db, patient_id, provider_id)
    if not assigned_patient:
        raise HTTPException(status_code=404, detail="Either patient or provider not found")
    return assigned_patient

@router.delete("/{patient_id}/remove-provider/{provider_id}", summary="Remove provider from patient")
def remove_provider_from_patient_route(patient_id: int, provider_id: int, db: Session = Depends(get_db)):
    updated_patient = remove_provider_from_patient(db, patient_id, provider_id)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Either patient or provider not found")
    return updated_patient

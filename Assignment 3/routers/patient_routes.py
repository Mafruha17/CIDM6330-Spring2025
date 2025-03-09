from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.connection import get_db
from database.crud.crud import (
    create_patient, get_patient, update_patient, delete_patient,
    assign_provider_to_patient, remove_provider_from_patient,
    assign_device_to_patient, remove_device_from_patient
)
from schemas.patient import PatientSchema

router = APIRouter(prefix="/patients", tags=["Patients"])

# ✅ Create a new Patient
@router.post("/", response_model=PatientSchema, summary="Create Patient")
def create_patient_route(patient: PatientSchema, db: Session = Depends(get_db)):
    return create_patient(db, patient)

# ✅ Get a Patient by ID (Includes Providers & Devices)
@router.get("/{patient_id}", response_model=PatientSchema, summary="Get Patient")
def get_patient_route(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# ✅ Update a Patient
@router.put("/{patient_id}", response_model=PatientSchema)
def update_patient_route(patient_id: int, patient_data: PatientSchema, db: Session = Depends(get_db)):
    updated_patient = update_patient(db, patient_id, patient_data)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient

# ✅ Delete a Patient (Cascades to Devices & Associations)
@router.delete("/{patient_id}", summary="Delete a Patient")
def delete_patient_route(patient_id: int, db: Session = Depends(get_db)):
    if not delete_patient(db, patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}

# ✅ Assign a Provider to a Patient (Many-to-Many)
@router.post("/{patient_id}/providers/{provider_id}", summary="Update Patient")
def assign_provider(patient_id: int, provider_id: int, db: Session = Depends(get_db)):
    patient = assign_provider_to_patient(db, patient_id, provider_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Provider not found")
    return patient

# ✅ Remove a Provider from a Patient
@router.delete("/{patient_id}/providers/{provider_id}")
def remove_provider(patient_id: int, provider_id: int, db: Session = Depends(get_db)):
    patient = remove_provider_from_patient(db, patient_id, provider_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Provider not found")
    return patient

# ✅ Assign a Device to a Patient (One-to-Many)
@router.post("/{patient_id}/devices/{device_id}")
def assign_device(patient_id: int, device_id: int, db: Session = Depends(get_db)):
    patient = assign_device_to_patient(db, patient_id, device_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Device not found")
    return patient

# ✅ Remove a Device from a Patient
@router.delete("/{patient_id}/devices/{device_id}")
def remove_device(patient_id: int, device_id: int, db: Session = Depends(get_db)):
    patient = remove_device_from_patient(db, patient_id, device_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Device not found")
    return patient

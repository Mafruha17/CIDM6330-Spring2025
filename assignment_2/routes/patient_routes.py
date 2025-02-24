from fastapi import APIRouter
from models.patient import Patient
from database.crud import create_patient, get_patient, update_patient, delete_patient

router = APIRouter()

@router.post("/patients/", response_model=Patient)
def create(patient: Patient):
    return create_patient(patient)

@router.get("/patients/{patient_id}", response_model=Patient)
def read(patient_id: int):
    return get_patient(patient_id)

@router.put("/patients/{patient_id}", response_model=Patient)
def update(patient_id: int, patient: Patient):
    return update_patient(patient_id, patient)

@router.delete("/patients/{patient_id}")
def delete(patient_id: int):
    return delete_patient(patient_id)

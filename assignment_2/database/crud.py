from fastapi import HTTPException
from models.patient import Patient
from database.connection import fake_db

# Create a new patient
def create_patient(patient: Patient):
    if patient.id in fake_db["patients"]:
        raise HTTPException(status_code=400, detail="Patient already exists")
    fake_db["patients"][patient.id] = patient
    return patient

# Retrieve a patient
def get_patient(patient_id: int):
    patient = fake_db["patients"].get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# Update an existing patient
def update_patient(patient_id: int, patient: Patient):
    if patient_id not in fake_db["patients"]:
        raise HTTPException(status_code=404, detail="Patient not found")
    fake_db["patients"][patient_id] = patient
    return patient

# Delete a patient
def delete_patient(patient_id: int):
    if patient_id not in fake_db["patients"]:
        raise HTTPException(status_code=404, detail="Patient not found")
    del fake_db["patients"][patient_id]
    return {"message": "Patient deleted successfully"}

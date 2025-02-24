from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Database simulation
fake_db: Dict[str, Dict] = {
    "patients": {},
    "healthcare_providers": {},
    "devices": {},
    "organizations": {},
    "data_processing": {},
    "authentication_service": {},
    "database": {},
    "device_manufacturer": {},
    "healthcare_platform": {},
    "device_frontend": {},
}

# Pydantic Models
class Patient(BaseModel):
    id: int
    name: str
    device_connected: bool

class HealthcareProvider(BaseModel):
    id: int
    name: str
    specialty: str

class Device(BaseModel):
    id: int
    type: str
    status: str

# CRUD Endpoints for Patients
@app.post("/patients/", response_model=Patient)
def create_patient(patient: Patient):
    if patient.id in fake_db["patients"]:
        raise HTTPException(status_code=400, detail="Patient already exists")
    fake_db["patients"][patient.id] = patient.dict()
    return patient

@app.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    patient = fake_db["patients"].get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, patient: Patient):
    if patient_id not in fake_db["patients"]:
        raise HTTPException(status_code=404, detail="Patient not found")
    fake_db["patients"][patient_id] = patient.dict()
    return patient

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    if patient_id not in fake_db["patients"]:
        raise HTTPException(status_code=404, detail="Patient not found")
    del fake_db["patients"][patient_id]
    return {"message": "Patient deleted successfully"}

# Similar CRUD operations can be implemented for other entities

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

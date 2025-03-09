from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.connection import get_db
from database.crud.device_crud import (
    create_device, get_device, update_device, delete_device, assign_device_to_patient
)
from schemas.device import DeviceSchema

router = APIRouter(prefix="/devices", tags=["Devices"])

# ✅ Create a new Device
@router.post("/", response_model=DeviceSchema, summary="Create Device")
def create_device_route(device: DeviceSchema, db: Session = Depends(get_db)):
    return create_device(db, device)

# ✅ Get a Device by ID
@router.get("/{device_id}", response_model=DeviceSchema, summary="Get Device")
def get_device_route(device_id: int, db: Session = Depends(get_db)):
    device = get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

# ✅ Update a Device
@router.put("/{device_id}", response_model=DeviceSchema, summary="Update Device")
def update_device_route(device_id: int, device_data: DeviceSchema, db: Session = Depends(get_db)):
    updated_device = update_device(db, device_id, device_data)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device

# ✅ Delete a Device
@router.delete("/{device_id}", summary="Delete Device")
def delete_device_route(device_id: int, db: Session = Depends(get_db)):
    if not delete_device(db, device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}

# ✅ Assign a Device to a Patient
@router.post("/{device_id}/assign/{patient_id}", summary="Assign Device to Patient")
def assign_device_route(device_id: int, patient_id: int, db: Session = Depends(get_db)):
    patient = assign_device_to_patient(db, patient_id, device_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Device not found")
    return patient

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
import traceback  # Import traceback to log errors

from database.connection import get_db
from schemas.device import DeviceSchema
from database.crud.device_crud import (
    create_device, get_device, get_all_devices, update_device, delete_device,
    assign_device_to_patient, remove_device_from_patient
)

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/", response_model=DeviceSchema, summary="Create a new device")
def create_device_route(device: DeviceSchema, db: Session = Depends(get_db)):
    """Create a new device."""
    try:
        return create_device(db, device)
    except Exception as e:
        print("❌ ERROR in `POST /devices/`")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
# ✅ Create a new Device

@router.get("/{device_id}", response_model=DeviceSchema, summary="Get a device by ID")
def get_device_route(device_id: int, db: Session = Depends(get_db)):
    """Retrieve a device by ID."""
    device = get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.get("/", response_model=List[DeviceSchema], summary="Get all devices")
def get_all_devices_route(db: Session = Depends(get_db)):
    """Retrieve all devices."""
    try:
        devices = get_all_devices(db)
        print(f"✅ DEBUG: Retrieved {len(devices)} devices.")  # Log count
        return devices
    except Exception as e:
        print("❌ ERROR in `GET /devices/`")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{device_id}", response_model=DeviceSchema, summary="Update a device")
def update_device_route(device_id: int, device_data: DeviceSchema, db: Session = Depends(get_db)):
    """Update a device."""
    updated_device = update_device(db, device_id, device_data)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device

@router.delete("/{device_id}", summary="Delete a device")
def delete_device_route(device_id: int, db: Session = Depends(get_db)):
    """Delete a device."""
    if not delete_device(db, device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully | or its stutus is inactive"}


@router.post("/{patient_id}/assign-device/{device_id}", summary="Assign device to patient")
def assign_device_to_patient_route(patient_id: int, device_id: int, db: Session = Depends(get_db)):
    """Assign a device to a patient with reassignment rules."""

    # Retrieve the device
    device = get_device(db, device_id)  # ✅ Correct
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Enforce reassignment rules
    if device.patient_id != 0 and device.patient_id != patient_id:
        raise HTTPException(status_code=400, detail="Device is already assigned to another patient")

    # Assign the device to the patient
    assigned_patient = assign_device_to_patient(db, patient_id, device_id)
    if not assigned_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return assigned_patient


@router.delete("/{patient_id}/remove-device/{device_id}", summary="Remove device from patient")
def remove_device_from_patient_route(patient_id: int, device_id: int, db: Session = Depends(get_db)):
    """Remove a device from a patient."""
    updated_patient = remove_device_from_patient(db, patient_id, device_id)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Either patient or device not found")
    return updated_patient

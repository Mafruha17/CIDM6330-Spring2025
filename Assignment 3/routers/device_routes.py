from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from database.connection import get_db
from schemas.device import DeviceSchema
from database.crud.device_crud import (
    create_device, get_device, get_all_devices, update_device, delete_device,
    assign_device_to_patient, remove_device_from_patient
)


router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/", response_model=DeviceSchema, summary="Create a new device")
def create_device_route(device: DeviceSchema, db: Session = Depends(get_db)):
    return create_device(db, device)


@router.get("/{device_id}", response_model=DeviceSchema, summary="Get a device by ID")
def get_device_route(device_id: int, db: Session = Depends(get_db)):
    device = get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.get("/", response_model=List[DeviceSchema], summary="Get all devices")
def get_all_devices_route(db: Session = Depends(get_db)):
    return get_all_devices(db)


@router.put("/{device_id}", response_model=DeviceSchema, summary="Update a device")
def update_device_route(device_id: int, device_data: DeviceSchema, db: Session = Depends(get_db)):
    updated_device = update_device(db, device_id, device_data)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device


@router.delete("/{device_id}", summary="Delete a device")
def delete_device_route(device_id: int, db: Session = Depends(get_db)):
    if not delete_device(db, device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}


@router.post("/{patient_id}/assign-device/{device_id}", summary="Assign device to patient")
def assign_device_to_patient_route(patient_id: int, device_id: int, db: Session = Depends(get_db)):
    assigned_patient = assign_device_to_patient(db, patient_id, device_id)
    if not assigned_patient:
        raise HTTPException(status_code=404, detail="Either patient or device not found")
    return assigned_patient


@router.delete("/{patient_id}/remove-device/{device_id}", summary="Remove device from patient")
def remove_device_from_patient_route(patient_id: int, device_id: int, db: Session = Depends(get_db)):
    updated_patient = remove_device_from_patient(db, patient_id, device_id)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Either patient or device not found")
    return updated_patient


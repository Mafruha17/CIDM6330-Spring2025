from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.crud.device_crud import (
    create_device, get_device, update_device, delete_device
)
from schemas.device import DeviceSchema

router = APIRouter(prefix="/devices", tags=["Devices"])

# ✅ Create a new Device
@router.post("/", response_model=DeviceSchema)
def create_device_route(device: DeviceSchema, db: Session = Depends(get_db)):
    return create_device(db, device)

# ✅ Get a Device by ID
@router.get("/{device_id}", response_model=DeviceSchema)
def get_device_route(device_id: int, db: Session = Depends(get_db)):
    device = get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

# ✅ Update a Device (Supports reassignment to another Patient)
@router.put("/{device_id}", response_model=DeviceSchema)
def update_device_route(device_id: int, device_data: DeviceSchema, db: Session = Depends(get_db)):
    updated_device = update_device(db, device_id, device_data)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device

# ✅ Delete a Device
@router.delete("/{device_id}")
def delete_device_route(device_id: int, db: Session = Depends(get_db)):
    if not delete_device(db, device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}

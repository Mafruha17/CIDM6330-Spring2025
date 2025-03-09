from sqlmodel import Session
from database.models import Device
from schemas.device import DeviceSchema
from repositories.device_repository import DeviceRepository
from typing import Optional, List

def create_device(db: Session, device_data: DeviceSchema) -> Device:
    return DeviceRepository(db).create(device_data.model_dump())

def get_device(db: Session, device_id: int) -> Optional[Device]:
    return DeviceRepository(db).get(device_id)

def get_all_devices(db: Session) -> List[Device]:
    return DeviceRepository(db).get_all()

def update_device(db: Session, device_id: int, device_data: DeviceSchema) -> Optional[Device]:
    return DeviceRepository(db).update(device_id, device_data.model_dump(exclude_unset=True))

def delete_device(db: Session, device_id: int) -> bool:
    return DeviceRepository(db).delete(device_id)

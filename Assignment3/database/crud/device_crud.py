from sqlmodel import Session, select
from database.models import Device, Patient
from schemas.device import DeviceSchema
from repositories.device_repository import DeviceRepository
from typing import Optional, List

def create_device(db: Session, device_data: DeviceSchema) -> Device:
    """Create a new device record."""
    return DeviceRepository(db).create(device_data.model_dump())

def get_device(db: Session, device_id: int) -> Optional[Device]:
    """Retrieve a device by its ID."""
    return DeviceRepository(db).get(device_id)

def get_all_devices(db: Session) -> List[Device]:
    """Retrieve all devices."""
    return DeviceRepository(db).get_all()

def update_device(db: Session, device_id: int, device_data: DeviceSchema) -> Optional[Device]:
    """Update an existing device record."""
    return DeviceRepository(db).update(device_id, device_data.model_dump(exclude_unset=True))

def delete_device(db: Session, device_id: int) -> bool:
    """Delete a device by its ID."""
    return DeviceRepository(db).delete(device_id)

def assign_device_to_patient(db: Session, patient_id: int, device_id: int):
    """Assign a device to a patient (One-to-Many relationship)."""
    patient_statement = select(Patient).where(Patient.id == patient_id)
    patient = db.exec(patient_statement).first()

    device_statement = select(Device).where(Device.id == device_id)
    device = db.exec(device_statement).first()

    if not patient or not device:
        return None  # Either patient or device not found

    if device in patient.devices:
        return patient  # Already assigned
    
    patient.devices.append(device)
    db.commit()
    db.refresh(patient)
    return patient

def remove_device_from_patient(db: Session, patient_id: int, device_id: int):
    """Remove a device from a patient (One-to-Many relationship)."""
    patient_statement = select(Patient).where(Patient.id == patient_id)
    patient = db.exec(patient_statement).first()

    device_statement = select(Device).where(Device.id == device_id)
    device = db.exec(device_statement).first()

    if not patient or not device:
        return None  # Not found

    if device not in patient.devices:
        return patient  # Device not assigned

    patient.devices.remove(device)
    db.commit()
    db.refresh(patient)
    return patient

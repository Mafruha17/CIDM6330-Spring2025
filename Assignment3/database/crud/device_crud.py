from sqlmodel import Session
from schemas.device import DeviceSchema
from database.models import Device, Patient
from repositories.device_repository import DeviceRepository
from repositories.patient_repository import PatientRepository
from typing import Optional, List
from sqlmodel import select

def create_device(db: Session, device_data: DeviceSchema) -> Device:
    return DeviceRepository(db).create(device_data)

def get_device(db: Session, device_id: int) -> Optional[Device]:
    return DeviceRepository(db).get(device_id)

def get_all_devices(db: Session) -> List[Device]:
    return DeviceRepository(db).get_all()

def update_device(db: Session, device_id: int, device_data: DeviceSchema) -> Optional[Device]:
    return DeviceRepository(db).update(device_id, device_data)

def delete_device(db: Session, device_id: int) -> bool:
    return DeviceRepository(db).delete(device_id)


def assign_device_to_patient(db: Session, patient_id: int, device_id: int):
    patient_repo = PatientRepository(db)
    device_repo = DeviceRepository(db)

    patient = patient_repo.get(patient_id)
    device = device_repo.get(device_id)

    if not patient or not device:
        return None  # Either record doesn't exist

    # Check if the device is already assigned
    if device.patient_id is not None:
        if device.patient_id == patient_id:
            # Already assigned to this patient, nothing to do
            return patient
        # Otherwise, it's assigned to a different patient – you could raise an error
        raise ValueError("Device is already assigned to a different patient")

    # Update the association
    device.patient_id = patient_id
    patient.devices.append(device)

    db.commit()
    db.refresh(patient)
    return patient


def remove_device_from_patient(db: Session, patient_id: int, device_id: int):
    patient_repo = PatientRepository(db)
    device_repo = DeviceRepository(db)

    patient = patient_repo.get(patient_id)
    device = device_repo.get(device_id)

    if not patient or not device:
        return None  # Either the patient or device doesn't exist

    # Check if the device is associated with this patient
    if device.patient_id != patient_id:
        # Optionally, you can raise an error or simply return the patient as-is
        return patient

    # Remove device from patient's device list if it's loaded
    if device in patient.devices:
        patient.devices.remove(device)
    
    # Reset the device's foreign key to break the association
    device.patient_id = None

    db.commit()
    db.refresh(patient)
    return patient


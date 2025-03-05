from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import Patient, Provider, Device
from schemas.patient import PatientSchema

# ✅ Create a new patient
def create_patient(db: Session, patient: PatientSchema):
    new_patient = Patient(**patient.model_dump())  # ✅ Fixed `.dict()` → `.model_dump()`
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

# ✅ Get a patient by ID (including related providers & devices)
def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

# ✅ Assign a provider to a patient (Many-to-Many)
def assign_provider_to_patient(db: Session, patient_id: int, provider_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    
    if not patient or not provider:
        return None
    
    if provider in patient.providers:
        return patient  # Already assigned

    patient.providers.append(provider)
    db.commit()
    return patient

# ✅ Assign a device to a patient (One-to-Many)
def assign_device_to_patient(db: Session, patient_id: int, device_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    device = db.query(Device).filter(Device.id == device_id).first()

    if not patient or not device:
        return None  # Either patient or device does not exist

    if device in patient.devices:
        return patient  # Already assigned, return as is

    patient.devices.append(device)  # Assign device to patient
    db.commit()
    return patient


# ✅ Update an existing patient (including assigned devices & providers)
def update_patient(db: Session, patient_id: int, patient_data: PatientSchema):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        return None  # Patient not found

    # ✅ Update patient attributes (excluding relationships)
    patient_dict = patient_data.model_dump(exclude_unset=True, exclude={"device_ids", "provider_ids"})
    for key, value in patient_dict.items():
        setattr(patient, key, value)

    # ✅ Update assigned devices if `device_ids` are provided
    if "device_ids" in patient_data.model_dump():
        new_devices = db.query(Device).filter(Device.id.in_(patient_data.device_ids)).all()
        patient.devices = new_devices  # Assign new device list

    # ✅ Update assigned providers if `provider_ids` are provided
    if "provider_ids" in patient_data.model_dump():
        new_providers = db.query(Provider).filter(Provider.id.in_(patient_data.provider_ids)).all()
        patient.providers = new_providers  # Assign new provider list

    db.commit()
    db.refresh(patient)
    return patient


# ✅ Remove a provider from a patient
def remove_provider_from_patient(db: Session, patient_id: int, provider_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not patient or not provider:
        return None

    if provider in patient.providers:
        patient.providers.remove(provider)
        db.commit()
    
    return patient

# ✅ Remove a device from a patient (One-to-Many)
def remove_device_from_patient(db: Session, patient_id: int, device_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    device = db.query(Device).filter(Device.id == device_id).first()

    if not patient or not device:
        return None  # Either patient or device does not exist

    if device in patient.devices:
        patient.devices.remove(device)  # Remove device from patient
        db.commit()

    return patient


def delete_patient(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Optional: Remove associations first (Many-to-Many)
    patient.providers = []
    patient.devices = []
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

from sqlalchemy.orm import Session
from database.models import Device, Patient
from schemas.device import DeviceSchema

# ✅ Create a new device
def create_device(db: Session, device: DeviceSchema):
    new_device = Device(**device.dict())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

# ✅ Get a device by ID
def get_device(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()

# ✅ Assign a device to a patient
def assign_device_to_patient(db: Session, device_id: int, patient_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not device or not patient:
        return None

    device.patient_id = patient_id
    db.commit()
    return device
# ✅ Update an existing device (Allows reassigning Patient)
def update_device(db: Session, device_id: int, device_data: DeviceSchema):
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        return None  # Device not found

    device_dict = device_data.model_dump(exclude_unset=True)

    # ✅ Check if `patient_id` is provided and reassign the device
    if "patient_id" in device_dict:
        new_patient = db.query(Patient).filter(Patient.id == device_dict["patient_id"]).first()
        if new_patient:
            device.patient = new_patient  # Reassign device to new patient

    for key, value in device_dict.items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)
    return device

# ✅ Delete a device
def delete_device(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if device:
        db.delete(device)
        db.commit()
        return True
    return False

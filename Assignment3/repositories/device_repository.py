from sqlmodel import Session, select
from schemas.device import DeviceSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List, Type

class DeviceRepository(BaseRepository[None, DeviceSchema]):
    """
    Repository for Device model operations.
    
    Note: The Device model's `patient_id` is optional so that a device can be created 
    independently and later associated with a patient.
    """
    device_model: Type = None  # Class-level variable to store the model

    def __init__(self, db: Session):
        from database.models import Device  # Import inside to avoid circular dependency
        super().__init__(db, Device)
        DeviceRepository.device_model = Device

    def create(self, obj_in: DeviceSchema) -> Optional[Type]:
        """
        Creates a new device record.
        
        Accepts a DeviceSchema that may optionally include a `patient_id`. If not provided,
        the device is created as unassigned.
        """
        obj_data = obj_in.model_dump(exclude_unset=True)
        # If 'patient_id' is not in obj_data, it defaults to None per the Device model.
        obj = self.device_model(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, item_id: int) -> Optional[Type]:
        statement = select(self.device_model).where(self.device_model.id == item_id)
        return self.db.exec(statement).first()

    def get_all(self) -> List[Type]:
        statement = select(self.device_model)
        return self.db.exec(statement).all()
    
    def delete(self, item_id: int, force: bool = False):
        """Soft-delete a device. If the device is assigned to a patient, 
        prevent deletion unless force=True."""
        # Retrieve the device record (using the ORM session or repository get)
        statement = select(self.device_model).where(self.device_model.id == item_id)
        device = self.db.exec(statement).first()
        #device = self.session.query(Device).get(device_id)
        if not  device :
            # Device not found – could raise an exception or return False
            raise ValueError(f"Device { item_id} not found")

        # 1. Check assignment to a patient
        if device.patient_id is not None:  
            # Device is currently assigned
            if not force:
                # 2. Prevent deletion if not forced
                raise RuntimeError("Device is assigned to a patient. Delete operation not allowed without force.")
            # If force=True, proceed despite the assignment (e.g., the caller knows what they’re doing)

        # 3. Perform soft delete by deactivating the device
        device.active = False
        self.session.commit()  # save change to the database
        self.db.refresh(device)  # Refresh the instance with updated values
        # Optionally, return the device or a confirmation
        return device
    #update

    def update(self, item_id: int, obj_in: DeviceSchema) -> Optional[Type]:
        statement = select(self.device_model).where(self.device_model.id == item_id)
        obj = self.db.exec(statement).first()
        if not obj:
            return None
        update_data = obj_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

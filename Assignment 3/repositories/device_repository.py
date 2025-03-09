from sqlalchemy.orm import Session
from database.models import Patient, Device, Provider
from schemas.patient import PatientSchema
from schemas.device import DeviceSchema
from schemas.provider import ProviderSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List
class DeviceRepository(BaseRepository[Device, DeviceSchema]):
    """Implements repository for Device entity using SQLAlchemy."""
    
    def __init__(self, db: Session):
        super().__init__(db, Device)
    
    def create(self, obj_in: DeviceSchema) -> Device:
        obj = Device(**obj_in.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def get(self, item_id: int) -> Optional[Device]:
        return self.db.query(Device).filter(Device.id == item_id).first()
    
    def get_all(self) -> List[Device]:
        return self.db.query(Device).all()
    
    def update(self, item_id: int, obj_in: DeviceSchema) -> Optional[Device]:
        obj = self.db.query(Device).filter(Device.id == item_id).first()
        if not obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, item_id: int) -> bool:
        obj = self.db.query(Device).filter(Device.id == item_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

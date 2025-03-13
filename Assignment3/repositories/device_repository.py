from sqlmodel import Session, select
from schemas.device import DeviceSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List, Type

class DeviceRepository(BaseRepository[None, DeviceSchema]):  
    device_model: Type = None  # Properly define class-level variable

    def __init__(self, db: Session):
        from database.models import Device  # Import inside to avoid circular import
        super().__init__(db, Device)
        DeviceRepository.device_model = Device  # Assign model to class variable

    def create(self, obj_in: DeviceSchema) -> Optional[Type]:  
        obj_data = obj_in.dict(exclude_unset=True)  # ✅ FIX: Use `.dict()`
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

    def update(self, item_id: int, obj_in: DeviceSchema) -> Optional[Type]:  
        statement = select(self.device_model).where(self.device_model.id == item_id)
        obj = self.db.exec(statement).first()
        if not obj:
            return None
        update_data = obj_in.dict(exclude_unset=True)  # ✅ Use `.dict()`
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

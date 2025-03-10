from sqlmodel import Session, select
from database.models import Device
from schemas.device import DeviceSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List

class DeviceRepository(BaseRepository[Device, DeviceSchema]):
    """Implements repository for Device entity using SQLModel."""

    def __init__(self, db: Session):
        super().__init__(db, Device)

    def create(self, obj_in: DeviceSchema) -> Device:
        obj = Device(**obj_in.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, item_id: int) -> Optional[Device]:
        statement = select(Device).where(Device.id == item_id)
        return self.db.exec(statement).first()

    def get_all(self) -> List[Device]:
        statement = select(Device)
        return self.db.exec(statement).all()

    def update(self, item_id: int, obj_in: DeviceSchema) -> Optional[Device]:
        statement = select(Device).where(Device.id == item_id)
        obj = self.db.exec(statement).first()
        if not obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

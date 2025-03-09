from sqlalchemy.orm import Session
from database.models import Patient, Device, Provider
from schemas.patient import PatientSchema
from schemas.device import DeviceSchema
from schemas.provider import ProviderSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List

class ProviderRepository(BaseRepository[Provider, ProviderSchema]):
    """Implements repository for Provider entity using SQLAlchemy."""
    
    def __init__(self, db: Session):
        super().__init__(db, Provider)
    
    def create(self, obj_in: ProviderSchema) -> Provider:
        obj = Provider(**obj_in.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def get(self, item_id: int) -> Optional[Provider]:
        return self.db.query(Provider).filter(Provider.id == item_id).first()
    
    def get_all(self) -> List[Provider]:
        return self.db.query(Provider).all()
    
    def update(self, item_id: int, obj_in: ProviderSchema) -> Optional[Provider]:
        obj = self.db.query(Provider).filter(Provider.id == item_id).first()
        if not obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, item_id: int) -> bool:
        obj = self.db.query(Provider).filter(Provider.id == item_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

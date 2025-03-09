from sqlalchemy.orm import Session
from database.models import Patient, Device, Provider
from schemas.patient import PatientSchema
from schemas.device import DeviceSchema
from schemas.provider import ProviderSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List

class PatientRepository(BaseRepository[Patient, PatientSchema]):
    """Implements repository for Patient entity using SQLAlchemy."""
    
    def __init__(self, db: Session):
        super().__init__(db, Patient)
    
    def create(self, obj_in: PatientSchema) -> Patient:
        obj = Patient(**obj_in.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def get(self, item_id: int) -> Optional[Patient]:
        return self.db.query(Patient).filter(Patient.id == item_id).first()
    
    def get_all(self) -> List[Patient]:
        return self.db.query(Patient).all()
    
    def update(self, item_id: int, obj_in: PatientSchema) -> Optional[Patient]:
        obj = self.db.query(Patient).filter(Patient.id == item_id).first()
        if not obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, item_id: int) -> bool:
        obj = self.db.query(Patient).filter(Patient.id == item_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

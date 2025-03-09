from sqlalchemy.orm import Session
from database.models import Patient, Device, Provider
from repositories.base_repository import BaseRepository

class SQLRepository(BaseRepository):
    """Implements repository using SQLAlchemy."""
    
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def create(self, data):
        obj = self.model(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, item_id: int):
        return self.db.query(self.model).filter(self.model.id == item_id).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def update(self, item_id: int, data):
        obj = self.db.query(self.model).filter(self.model.id == item_id).first()
        if not obj:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, item_id: int):
        obj = self.db.query(self.model).filter(self.model.id == item_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

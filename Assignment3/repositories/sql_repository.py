from sqlmodel import Session, select
from database.models import Patient, Device, Provider
from repositories.base_repository import BaseRepository

class SQLRepository(BaseRepository):
    """
    A generic repository using SQLModel for an arbitrary model.
    In practice, you might use your specialized repos (e.g. PatientRepository),
    but here's a fallback for general usage.
    """

    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def create(self, data):
        obj = self.model(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, item_id: int):
        statement = select(self.model).where(self.model.id == item_id)
        return self.db.exec(statement).first()

    def get_all(self):
        statement = select(self.model)
        return self.db.exec(statement).all()

    def update(self, item_id: int, data):
        statement = select(self.model).where(self.model.id == item_id)
        obj = self.db.exec(statement).first()
        if not obj:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, item_id: int):
        statement = select(self.model).where(self.model.id == item_id)
        obj = self.db.exec(statement).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

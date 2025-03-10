from sqlmodel import Session, select
from database.models import Provider
from schemas.provider import ProviderSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List

class ProviderRepository(BaseRepository[Provider, ProviderSchema]):
    """
    Implements repository for Provider entity using SQLModel / Session.
    """

    def __init__(self, db: Session):
        super().__init__(db, Provider)

    def create(self, obj_in: ProviderSchema) -> Provider:
        obj = Provider(**obj_in.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, item_id: int) -> Optional[Provider]:
        statement = select(Provider).where(Provider.id == item_id)
        return self.db.exec(statement).first()

    def get_all(self) -> List[Provider]:
        statement = select(Provider)
        return self.db.exec(statement).all()

    def update(self, item_id: int, obj_in: ProviderSchema) -> Optional[Provider]:
        statement = select(Provider).where(Provider.id == item_id)
        obj = self.db.exec(statement).first()
        if not obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, item_id: int) -> bool:
        statement = select(Provider).where(Provider.id == item_id)
        obj = self.db.exec(statement).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

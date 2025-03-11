from sqlmodel import Session, select
from database.models import Provider
from schemas.provider import ProviderSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List

class ProviderRepository(BaseRepository[Provider, ProviderSchema]):
    def __init__(self, db: Session):
        super().__init__(db, Provider)

    def create(self, obj_in: ProviderSchema) -> Provider:
        provider = Provider(**obj_in.dict())
        self.db.add(provider)
        self.db.commit()
        self.db.refresh(provider)
        return provider

    def get(self, provider_id: int) -> Optional[Provider]:
        statement = select(Provider).where(Provider.id == provider_id)
        return self.db.exec(statement).first()

    def get_all(self) -> list[Provider]:
        statement = select(Provider)
        return self.db.exec(statement).all()

    def update(self, provider_id: int, obj_in: ProviderSchema) -> Optional[Provider]:
        provider = self.get(provider_id)
        if not provider:
            return None
        update_data = obj_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(provider, key, value)
        self.db.commit()
        self.db.refresh(provider)
        return provider

    def delete(self, provider_id: int) -> bool:
        provider = self.get(provider_id)
        if provider:
            self.db.delete(provider)
            self.db.commit()
            return True
        return False

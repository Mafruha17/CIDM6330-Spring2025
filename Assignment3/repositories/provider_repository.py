from sqlmodel import Session, select
from schemas.provider import ProviderSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List, Type

class ProviderRepository(BaseRepository[None, ProviderSchema]):  
    provider_model: Type = None  # Class-level variable to store the model

    def __init__(self, db: Session):
        from database.models import Provider  # Import inside method to prevent circular import
        super().__init__(db, Provider)
        self.provider_model = Provider  # Assign model to instance variable

    def create(self, obj_in: ProviderSchema) -> Optional[Type]:
        obj = self.provider_model(**obj_in.model_dump())  # Use instance variable
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, provider_id: int) -> Optional[Type]:
        statement = select(self.provider_model).where(self.provider_model.id == provider_id)
        return self.db.exec(statement).first()

    #def get_all(self) -> List[Type]:
      #  statement = select(self.provider_model)
      #  return self.db.exec(statement).all()
    
    def get_all(self) -> List[ProviderSchema]:
        statement = select(self.provider_model)
        results = self.db.exec(statement).all()
        return [ProviderSchema.model_validate(obj) for obj in results]


    def update(self, provider_id: int, obj_in: ProviderSchema) -> Optional[Type]:
        statement = select(self.provider_model).where(self.provider_model.id == provider_id)
        obj = self.db.exec(statement).first()
        if not obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, provider_id: int) -> bool:
        obj = self.get(provider_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

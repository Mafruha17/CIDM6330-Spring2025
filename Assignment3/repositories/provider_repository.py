from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from schemas.provider import ProviderSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List, Type
from database.models import Provider

class ProviderRepository(BaseRepository[None, ProviderSchema]):  
    provider_model: Type = None  # Class-level variable to store the model

    def __init__(self, db: Session):
        from database.models import Provider  # Import inside to prevent circular import
        super().__init__(db, Provider)
        self.provider_model = Provider  # Assign model to instance variable

    def create(self, obj_in: ProviderSchema) -> Optional[Type]:
        obj_data = obj_in.model_dump(exclude_unset=True)
        provider = self.provider_model(**obj_data)
        self.db.add(provider)
        self.db.commit()
        self.db.refresh(provider)
        return provider
    
    def get(self, provider_id: int) -> Optional[Provider]:
        statement = (
            select(self.provider_model)
            .options(selectinload(self.provider_model.patients))
            .where(self.provider_model.id == provider_id)
        )
        return self.db.exec(statement).first()

   
    def get_all(self) -> List[ProviderSchema]:
        """
        Retrieves all providers, converting them into ProviderSchema objects
        so they include the 'patients' list if present.
        """
        provider = (
            select(self.provider_model)
            .options(selectinload(self.provider_model.patients))
        )
        results = self.db.exec(provider).all()

        # Convert each ORM object to ProviderSchema so it includes the 'patients' data
        return [
            ProviderSchema.model_validate(obj)
            for obj in results
        ]


    def update(self, provider_id: int, obj_in: ProviderSchema) -> Optional[Type]:
        """
        Updates an existing provider by ID with the given ProviderSchema data.
        """
        statement = select(self.provider_model).where(self.provider_model.id == provider_id)
        provider = self.db.exec(statement).first()
        if not provider:
            return None

        update_data = obj_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(provider, key, value)
        self.db.commit()
        self.db.refresh(provider)
        return provider


    def delete(self, provider_id: int) -> bool:
        """
        Deletes a provider by ID from the database.
        If you want to prevent deletion if they have linked patients, you can add checks here.
        """
        provider = self.get(provider_id)
        if provider:
            self.db.delete(provider)
            self.db.commit()
            return True
        return False
    
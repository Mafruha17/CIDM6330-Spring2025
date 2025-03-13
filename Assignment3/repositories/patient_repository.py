from sqlmodel import Session, select
from schemas.patient import PatientSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List, Type
from database.models import Patient  # Ensure the correct import

class PatientRepository(BaseRepository[None, PatientSchema]):  
    def __init__(self, db: Session):
        super().__init__(db, Patient)

    def create(self, obj_in: PatientSchema) -> Optional[Patient]:
        """
        Converts schema to dictionary before saving.
        Ensures compatibility between Pydantic versions.
        """
        obj_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, "dict") else obj_in.dict(exclude_unset=True)
        obj = Patient(**obj_data)  
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, patient_id: int) -> Optional[Patient]:
        statement = select(Patient).where(Patient.id == patient_id)
        return self.db.exec(statement).first()

    def get_all(self) -> List[Patient]:
        statement = select(Patient)
        return self.db.exec(statement).all()

    def update(self, patient_id: int, obj_in: PatientSchema) -> Optional[Patient]:
        """
        Update a patient without modifying the ID.
        """
        statement = select(Patient).where(Patient.id == patient_id)
        obj = self.db.exec(statement).first()
        if not obj:
            return None  # Patient not found

        # Extract updated fields (excluding `id`)
        update_data = obj_in.dict(exclude_unset=True, exclude={"id"}) if hasattr(obj_in, "dict") else obj_in.dict(exclude_unset=True, exclude={"id"})

        # Apply updates to the existing object
        for key, value in update_data.items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj  # Return the updated patient model directly

    def delete(self, patient_id: int) -> bool:
        obj = self.get(patient_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

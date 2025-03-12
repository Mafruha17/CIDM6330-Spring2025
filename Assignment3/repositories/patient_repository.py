
#from database.models import Patient  # Ensure proper import
from sqlmodel import Session, select
from schemas.patient import PatientSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List, Type

class PatientRepository(BaseRepository[None, PatientSchema]):  
    patient_model: Type = None  

    def __init__(self, db: Session):
        from database.models import Patient  
        super().__init__(db, Patient)
        PatientRepository.patient_model = Patient  

    def create(self, obj_in: PatientSchema) -> Optional[Type]:
        """
        Converts schema to dictionary before saving.
        Ensures compatibility between Pydantic versions.
        """
        obj_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, "dict") else obj_in.model_dump(exclude_unset=True)
        obj = self.patient_model(**obj_data)  
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, patient_id: int) -> Optional[Type]:
        statement = select(self.patient_model).where(self.patient_model.id == patient_id)
        return self.db.exec(statement).first()

    def get_all(self) -> List[PatientSchema]:
        statement = select(self.patient_model)
        results = self.db.exec(statement).all()
        
        # Adjust based on Pydantic version
        return [PatientSchema.parse_obj(obj) if hasattr(PatientSchema, "parse_obj") else PatientSchema.model_validate(obj) for obj in results]

    def update(self, patient_id: int, obj_in: PatientSchema) -> Optional[PatientSchema]:
        statement = select(self.patient_model).where(self.patient_model.id == patient_id)
        obj = self.db.exec(statement).first()
        if not obj:
            return None

        update_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, "dict") else obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        
        return PatientSchema.parse_obj(obj) if hasattr(PatientSchema, "parse_obj") else PatientSchema.model_validate(obj)

    def delete(self, patient_id: int) -> bool:
        obj = self.get(patient_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

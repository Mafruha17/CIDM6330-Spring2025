from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from schemas.patient import PatientSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List, Type
from database.models import Patient  # Ensure the correct import

class PatientRepository(BaseRepository[None, PatientSchema]):  
    def __init__(self, db: Session):
        super().__init__(db, Patient)

    def create(self, obj_in: PatientSchema) -> Optional[Patient]:
       
        obj_data = obj_in.model_dump(exclude_unset=True)  #if hasattr(obj_in, "dict") else obj_in.dict(exclude_unset=True)
        obj = Patient(**obj_data)  
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, patient_id: int) -> Optional[Patient]:
        # Eagerly load devices (and providers if needed)
        statement = (
            select(Patient)
            .options(selectinload(Patient.devices))  # Load related devices
            .options(selectinload(Patient.providers))  # Load related providers, if defined
            .where(Patient.id == patient_id)
        )
        return self.db.exec(statement).first()
    
    def get_all(self) -> List[Patient]:
        # Eagerly load relationships for all patients
        statement = (
            select(Patient)
            .options(selectinload(Patient.devices))
            .options(selectinload(Patient.providers))
        )
        return self.db.exec(statement).all()
    
    def update(self, patient_id: int, obj_in: PatientSchema) -> Optional[Patient]:
        statement = select(Patient).where(Patient.id == patient_id)
        patient = self.db.exec(statement).first()
        if not patient:
            return None  # Patient not found

        # Extract updated fields, excluding the id
        update_data = obj_in.model_dump(exclude_unset=True, exclude={"id"})
        for key, value in update_data.items():
            setattr(patient, key, value)

        self.db.commit()
        self.db.refresh(patient)
        return patient
    
   # may need to check this code
    def delete(self, patient_id: int, force: bool = False) -> bool:
        patient = self.get(patient_id)
        if not patient:
            return False  # Patient not found

        # Check for associations. If there are associated devices or providers, do not allow deletion unless forced.
        if (patient.devices or patient.providers) and not force:
            raise RuntimeError("Patient has associated devices or providers. Delete operation not allowed without force.")

        self.db.delete(patient)
        self.db.commit()
        return True

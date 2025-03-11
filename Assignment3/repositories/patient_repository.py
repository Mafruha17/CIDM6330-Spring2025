from sqlmodel import Session, select
from database.models import Patient
from schemas.patient import PatientSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List

class PatientRepository(BaseRepository[Patient, PatientSchema]):
    def __init__(self, db: Session):
        super().__init__(db, Patient)

    def create(self, obj_in: PatientSchema) -> Patient:
        patient = Patient(**obj_in.dict())
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def get(self, patient_id: int) -> Optional[Patient]:
        statement = select(Patient).where(Patient.id == patient_id)
        return self.db.exec(statement).first()

    def get_all(self) -> List[Patient]:
        statement = select(Patient)
        return self.db.exec(statement).all()

    def update(self, patient_id: int, patient_data: PatientSchema) -> Optional[Patient]:
        patient = self.get(patient_id)
        if not patient:
            return None
        update_data = patient_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(patient, key, value)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def delete(self, patient_id: int) -> bool:
        patient = self.get(patient_id)
        if patient:
            self.db.delete(patient)
            self.db.commit()
            return True
        return False

    def get(self, patient_id: int) -> Optional[Patient]:
        return self.db.exec(select(Patient).where(Patient.id == patient_id)).first()


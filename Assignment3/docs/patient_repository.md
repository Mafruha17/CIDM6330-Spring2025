# **Patient Repository Documentation**

## **Overview**
The **Patient Repository** is responsible for handling all CRUD operations related to patients. It abstracts database interactions and allows the API to interact with **multiple storage backends** (SQLModel, CSV, and In-Memory) without modifying the API routes.

This repository follows the **Repository Pattern**, ensuring modularity and flexibility in data persistence.

---

## **Implementation Details**
The repository is implemented in **`repositories/patient_repository.py`** and extends the **Base Repository**.

### **✅ Patient Repository Code (`patient_repository.py`)**
```python
from sqlmodel import Session, select
from schemas.patient import PatientSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List, Type
from database.models import Patient

class PatientRepository(BaseRepository[Patient, PatientSchema]):  
    def __init__(self, db: Session):
        super().__init__(db, Patient)  

    def create(self, obj_in: PatientSchema) -> Optional[Patient]:
        obj_data = obj_in.dict(exclude_unset=True)
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
        obj = self.get(patient_id)
        if not obj:
            return None
        update_data = obj_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, patient_id: int) -> bool:
        obj = self.get(patient_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
```

---

## **Key Features**
- **Encapsulates all CRUD operations for patients.**
- **Uses `BaseRepository` to enforce consistency across repositories.**
- **Supports multiple storage backends (SQL, CSV, In-Memory).**
- **Ensures compatibility with FastAPI dependency injection.**

---

## **Usage in FastAPI Routes**
The **Patient Repository** is used inside `patient_routes.py` via dependency injection:

```python
@router.post("/")
def create_patient_route(patient: PatientSchema, db: Session = Depends(get_db)):
    return PatientRepository(db).create(patient)
```

---

## **Conclusion**
The **Patient Repository** ensures **modular, scalable, and maintainable** patient data management by following the **Repository Pattern**. It allows seamless integration with different data storage backends, making the system flexible and efficient.


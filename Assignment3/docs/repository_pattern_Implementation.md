# **Repository Documentation**

## **Overview**
This document provides an overview of the **Repository Pattern** implemented in **Assignment 03**. The repositories act as an abstraction layer between the **API (FastAPI)** and the **underlying data storage**. This allows seamless switching between different persistence mechanisms (**SQLModel, CSV, and In-Memory**) without modifying the business logic.

The repositories are designed to handle **CRUD operations** for **Patients, Providers, and Devices** while ensuring data consistency.

---

## **Table of Contents**
1. [Repository Pattern & Implementation](#repository-pattern--implementation)
2. [Base Repository](#base-repository-repositoriesbase_repositorypy)
3. [SQLModel Repository](#sqlmodel-repository-repositoriessql_repositorypy)
4. [CSV Repository](#csv-repository-repositoriescsv_repositorypy)
5. [In-Memory Repository](#in-memory-repository-repositoriesin_memory_repositorypy)
6. [Patient Repository](#patient-repository)
7. [Provider Repository](#provider-repository)
8. [Device Repository](#device-repository)
9. [Switching Between Repositories](#switching-between-repositories)
10. [Conclusion](#conclusion)

---

## **1. Repository Pattern & Implementation**
The **Repository Pattern** is implemented to:
- **Abstract data access logic** from API routes.
- **Ensure modularity** by keeping persistence logic separate from business logic.
- **Support multiple storage backends** (SQL database, CSV file, In-Memory storage).
- **Improve testability** by allowing unit tests to run against an in-memory repository.

Each repository follows a common interface, allowing interchangeable usage of storage backends.

---

## **2. Base Repository (`repositories/base_repository.py`)**
The base repository defines a **generic interface** for handling CRUD operations. All other repositories extend this class.

### **✅ Base Repository Implementation**
```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlmodel import Session, select

T = TypeVar("T")  # The ORM model type (e.g., Patient, Provider, etc.)
S = TypeVar("S")  # The Pydantic/SQLModel schema type

class BaseRepository(ABC, Generic[T, S]):
    def __init__(self, db: Session, model: T):
        self.db = db
        self.model = model

    @abstractmethod
    def create(self, data: S) -> T:
        pass

    def get(self, item_id: int) -> Optional[T]:
        statement = select(self.model).where(self.model.id == item_id)
        return self.db.exec(statement).first()

    def get_all(self) -> List[T]:
        statement = select(self.model)
        return self.db.exec(statement).all()

    @abstractmethod
    def update(self, item_id: int, data: S) -> Optional[T]:
        pass

    def delete(self, item_id: int) -> bool:
        statement = select(self.model).where(self.model.id == item_id)
        obj = self.db.exec(statement).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
```

---

## **3. SQLModel Repository (`repositories/sql_repository.py`)**
This repository handles **SQL database persistence** using **SQLModel + SQLAlchemy ORM**.

### **✅ Implementation**
```python
from sqlmodel import Session, select
from database.models import Patient, Device, Provider
from repositories.base_repository import BaseRepository

class SQLRepository(BaseRepository):
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def create(self, data):
        obj = self.model(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
```

---

## **4. CSV Repository (`repositories/csv_repository.py`)**
This repository **stores and retrieves data from CSV files** instead of a relational database.

### **✅ Implementation**
```python
import csv
import os
from typing import List, Optional, Dict
from repositories.base_repository import BaseRepository

class CSVRepository(BaseRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.fieldnames = ["id", "name", "email"]
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
```

---

## **5. In-Memory Repository (`repositories/in_memory_repository.py`)**
This repository **stores data in Python dictionaries**, making it useful for unit testing.

### **✅ Implementation**
```python
from typing import Dict, List, Optional
from repositories.base_repository import BaseRepository

class InMemoryRepository(BaseRepository):
    def __init__(self):
        self.data: Dict[int, dict] = {}
        self.current_id = 1
```
Each repository follows a common interface, allowing interchangeable usage of storage backends.

---
---
## **6. Patient Repository (`repositories/patient_repository.py`)**
Manages CRUD operations for patient entities.

### **✅ Implementation**
```python
from sqlmodel import Session, select
from database.models import Patient
from schemas.patient import PatientSchema
from repositories.base_repository import BaseRepository

class PatientRepository(BaseRepository[Patient, PatientSchema]):
    def __init__(self, db: Session):
        super().__init__(db, Patient)

    def create(self, obj_in: PatientSchema) -> Patient:
        obj = Patient(**obj_in.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
```

---

## **7. Provider Repository (`repositories/provider_repository.py`)**
Manages CRUD operations for provider entities.

### **✅ Implementation**
```python
from sqlmodel import Session, select
from database.models import Provider
from schemas.provider import ProviderSchema
from repositories.base_repository import BaseRepository

class ProviderRepository(BaseRepository[Provider, ProviderSchema]):
    def __init__(self, db: Session):
        super().__init__(db, Provider)

    def create(self, obj_in: ProviderSchema) -> Provider:
        obj = Provider(**obj_in.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
```

---

## **8. Device Repository (`repositories/device_repository.py`)**
Manages CRUD operations for device entities.

### **✅ Implementation**
```python
from sqlmodel import Session, select
from database.models import Device
from schemas.device import DeviceSchema
from repositories.base_repository import BaseRepository

class DeviceRepository(BaseRepository[Device, DeviceSchema]):
    def __init__(self, db: Session):
        super().__init__(db, Device)

    def create(self, obj_in: DeviceSchema) -> Device:
        obj = Device(**obj_in.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
```

---

## **9. Switching Between Repositories**
To switch repositories, update the `.env` file:
```
REPO_TYPE=sql  # Options: sql, csv, memory
```

---

## **10. Conclusion**
- The repository pattern abstracts data access, ensuring flexibility and maintainability.
- Supports multiple storage backends (SQL, CSV, In-Memory) with minimal API changes.
- Encapsulates CRUD operations, keeping FastAPI routes clean and modular.

By implementing the Repository Pattern, this project achieves separation of concerns, testability, and easy adaptability across different persistence layers. 🚀



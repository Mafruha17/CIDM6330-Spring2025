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
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")  # Represents a database model class
S = TypeVar("S")  # Represents a Pydantic schema

class BaseRepository(Generic[T, S]):
    def __init__(self, db, model: T):
        self.db = db
        self.model = model

    def create(self, obj_in: S) -> T:
        obj = self.model(**obj_in.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, item_id: int) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == item_id).first()

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def update(self, item_id: int, obj_in: S) -> Optional[T]:
        obj = self.get(item_id)
        if not obj:
            return None
        update_data = obj_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, item_id: int) -> bool:
        obj = self.get(item_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
```

### **🔹 Key Features:**
- **Defines common CRUD operations**.
- **Uses Generics (`T, S`)** to support different models and schemas.
- **Provides a structured way to interact with repositories.**

---

## **3. SQLModel Repository (`repositories/sql_repository.py`)**
This repository handles **SQL database persistence** using **SQLModel + SQLAlchemy ORM**.

### **✅ Implementation**
```python
from sqlmodel import Session, select
from database.models import Patient
from schemas.patient import PatientSchema
from repositories.base_repository import BaseRepository

class SQLPatientRepository(BaseRepository[Patient, PatientSchema]):
    def __init__(self, db: Session):
        super().__init__(db, Patient)
```

### **🔹 Key Features:**
- **Handles CRUD operations using SQLAlchemy ORM.**
- **Supports transactions to ensure data integrity.**
- **Uses dependency injection (`Depends(get_db)`) in API routes.**

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

    def get_all(self) -> List[Dict[str, str]]:
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            return list(csv.DictReader(file))
```

### **🔹 Key Features:**
- **Stores and retrieves data from CSV files.**
- **Simple persistence mechanism without requiring a database.**
- **Useful for lightweight applications and debugging.**

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

    def create(self, obj_in) -> dict:
        item_dict = obj_in.dict()
        item_dict["id"] = self.current_id
        self.data[self.current_id] = item_dict
        self.current_id += 1
        return item_dict

    def get_all(self) -> List[dict]:
        return list(self.data.values())
```

### **🔹 Key Features:**
- **Stores data in an in-memory Python dictionary.**
- **Allows quick testing without a database connection.**
- **Data is lost when the application restarts.**

---
## **6. Patient Repository**
For more details, refer to the [Patient Repository](docs/patient_repository.md).

## **7. Provider Repository**
For more details, refer to the [Provider Repository](docs/provider_repository.md).

## **8. Device Repository**
For more details, refer to the [Device Repository](docs/device_repository.md).

---

## **9. Switching Between Repositories**
FastAPI dynamically selects the repository based on environment variables:
```python
import os
from repositories.sql_repository import SQLPatientRepository
from repositories.csv_repository import CSVRepository
from repositories.in_memory_repository import InMemoryRepository

def get_patient_repository():
    repo_type = os.getenv("REPO_TYPE", "sql")
    if repo_type == "csv":
        return CSVRepository()
    elif repo_type == "memory":
        return InMemoryRepository()
    else:
        return SQLPatientRepository()
```
To switch repositories, update the `.env` file:
```
REPO_TYPE=sql  # Options: sql, csv, memory
```

---

## **Conclusion**
- **The repository pattern abstracts data access**, ensuring **flexibility and maintainability**.
- **Supports multiple storage backends** (SQL, CSV, In-Memory) with minimal API changes.
- **Encapsulates CRUD operations**, keeping FastAPI routes clean and modular.
- **Provides a scalable approach** for handling complex data persistence needs.

By implementing the **Repository Pattern**, this project achieves **separation of concerns, testability, and easy adaptability** across different persistence layers. 🚀


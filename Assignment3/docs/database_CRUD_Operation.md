# **Database Documentation**

## **Overview**

This document describes the database structure and CRUD (Create, Read, Update, Delete) operations used in **Assignment 03** for managing **Patients, Providers, and Devices** in a FastAPI application. The database implementation supports multiple storage mechanisms (**SQLModel, CSV, and In-Memory**), following the **Repository Pattern**.

---

## **1. Database Models (`database/models.py`)**

The database models define the schema for **patients, providers, and devices** using **SQLModel**, which integrates Pydantic validation with SQLAlchemy ORM.

### **🔹 Patient Model (`database/models.py`)**
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class PatientProviderLink(SQLModel, table=True):
    patient_id: int = Field(foreign_key="patient.id", primary_key=True)
    provider_id: int = Field(foreign_key="provider.id", primary_key=True)

class Provider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    specialty: str
    patients: List["Patient"] = Relationship(back_populates="providers", link_model=PatientProviderLink)

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    age: int
    active: bool = Field(default=True)
    providers: List["Provider"] = Relationship(back_populates="patients", link_model=PatientProviderLink)
    devices: List["Device"] = Relationship(back_populates="patient")

class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    serial_number: str = Field(unique=True)
    active: bool = Field(default=True)
    patient_id: Optional[int] = Field(default=None, foreign_key="patient.id")
    patient: Optional["Patient"] = Relationship(back_populates="devices")
```

---

## **2. Database Connection (`database/connection.py`)**

This module handles database connection and session management.

```python
import os
from sqlmodel import Session, create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/database.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

def get_db():
    with Session(engine) as session:
        yield session
```

---

## **3. Database Initialization (`database/create_db.py`)**

```python
import os
import sqlite3
from sqlmodel import SQLModel
from database.connection import engine
from database.models import Device, Patient, Provider, PatientProviderLink

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def create_tables():
    print("\n🚀 Creating database tables...")
    try:
        SQLModel.metadata.drop_all(bind=engine)
        print("🗑️ Dropped existing tables!")
        SQLModel.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

def verify_tables():
    print("\n🔍 Verifying existing tables in database.db...")
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        if tables:
            print(f"✅ Existing tables: {[table[0] for table in tables]}")
        else:
            print("⚠️ No tables found in the database.")
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print("🗑️ Old database file removed.")
    create_tables()
    verify_tables()
```

---

## **4. CRUD Operations (`database/crud/`)**

### **🔹 Patient CRUD (`database/crud/patient_crud.py`)**
```python
from sqlmodel import Session
from database.models import Patient
from repositories.patient_repository import PatientRepository
from schemas.patient import PatientSchema

def create_patient(db: Session, patient_data: PatientSchema) -> Patient:
    return PatientRepository(db).create(patient_data)

def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return PatientRepository(db).get(patient_id)
```

---

### **🔹 Provider CRUD (`database/crud/provider_crud.py`)**
```python
from sqlmodel import Session
from database.models import Provider
from repositories.provider_repository import ProviderRepository
from schemas.provider import ProviderSchema

def create_provider(db: Session, provider_data: ProviderSchema) -> Provider:
    return ProviderRepository(db).create(provider_data.model_dump(exclude_unset=True))
```

---

### **🔹 Device CRUD (`database/crud/device_crud.py`)**
```python
from sqlmodel import Session
from database.models import Device
from repositories.device_repository import DeviceRepository
from schemas.device import DeviceSchema

def create_device(db: Session, device_data: DeviceSchema) -> Device:
    return DeviceRepository(db).create(device_data)
```

---

## **Conclusion**

- The **database models** provide the core structure for Patient, Provider, and Device entities.
- **CRUD functions** ensure data management across repositories.
- **The repository pattern** abstracts data access, ensuring **API flexibility** across multiple storage options.
- **SQLModel ORM** provides seamless database interactions while maintaining **Pydantic validation.**

This documentation serves as a reference for managing database operations within the **FastAPI Repository Pattern**. 🚀


Below is the updated Markdown document with a new "Summary" section at the very end. This section briefly describes what the document contains, serving as a final recap.

---

```markdown
**West Texas A&M University**  
**Semester:** Spring 2025  
**Course:** CIDM6330/01 Software Engineering  
**Student:** Nobolayra and Aiden  

---

# Assignment 02: From Specification to API

This project provides a RESTful API using FastAPI to manage healthcare-related entities, including Patients, Devices, and Providers. It enables users to perform CRUD operations efficiently while ensuring data integrity through proper entity relationships and validation.

---

<details>
  <summary><strong>Table of Contents</strong></summary>

- [Installation & Setup](#installation--setup)
- [Environment Configuration](#environment-configuration)
- [Project Folder Structure](#project-folder-structure)
- [API Endpoints](#api-endpoints)
  - [Patient Routes](#patient-routes)
  - [Device Routes](#device-routes)
  - [Provider Routes](#provider-routes)
- [Enhancing Database Relationships, Incorporating All Entities, and Optimizing Queries for Efficiency](#enhancing-database-relationships-incorporating-all-entities-and-optimizing-queries-for-efficiency)
- [Steps I Follow to Optimize | Minimize ERD](#steps-i-follow-to-optimize--minimize-erd)
- [Introducing Object-Oriented Concepts in ERD Design](#introducing-object-oriented-concepts-in-erd-design)
- [What If I Encounter a Recursive Relationship?](#what-if-i-encounter-a-recursive-relationship)
- [Handling Validation Errors](#handling-validation-errors)
- [CRUD Implementation](#crud-implementation)
- [Notes](#notes)
- [Future Implementations Would Be Good to Have](#future-implementations-would-be-good-to-have)
- [Conclusion](#conclusion)
- [Summary](#summary)
- [Code Implementation](#code-implementation)
</details>

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_name>
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

<details>
<summary>Windows (PowerShell)</summary>

```bash
.\venv\Scripts\Activate
```
</details>

<details>
<summary>macOS/Linux</summary>

```bash
source venv/bin/activate
```
</details>

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Setup Database

```bash
rm database/database.db  # Remove old DB if it exists
python database/create_db.py  # Create new DB
```

### 6. Run the API Server

```bash
uvicorn main:app --reload
```

---

## Environment Configuration

The project uses a `.env` file to manage environment variables. Ensure you create a `.env` file in the project root with the following content (or update it as needed):

```env
# .env file

# Database connection URL (defaults to SQLite if not set)
DATABASE_URL=sqlite:///./database.db
```

---

## Project Folder Structure

```plaintext
project-root/
│
│-- database/
│   ├── crud/
│   │    ├── device_crud.py      # CRUD functions for Devices
│   │    ├── patient_crud.py     # CRUD functions for Patients
│   │    └── provider_crud.py    # CRUD functions for Providers
│   ├── connection.py           # Database connection settings
│   ├── create_db.py            # Script to initialize database
│   ├── models.py               # ORM models for tables
│   └── database.db             # SQLite database file
│
│-- routers/
│   ├── device_routes.py        # API routes for Device CRUD
│   ├── patient_routes.py       # API routes for Patient CRUD
│   └── provider_routes.py      # API routes for Provider CRUD
│
│-- schemas/
│   ├── device.py               # Pydantic schemas for Devices
│   ├── patient.py              # Pydantic schemas for Patients
│   └── provider.py             # Pydantic schemas for Providers
│
├── main.py                     # FastAPI main entry file
├── requirements.txt            # Python dependencies
└── Assignment2.md              # Project Documentation
```

---

## API Endpoints

### Patient Routes

- **POST** `/patients/`  
  Create a new patient

- **GET** `/patients/{patient_id}`  
  Retrieve patient details

- **PUT** `/patients/{patient_id}`  
  Update patient details

- **DELETE** `/patients/{patient_id}`  
  Delete a patient

### Device Routes

- **POST** `/devices/`  
  Create a new device

- **GET** `/devices/{device_id}`  
  Retrieve device details

- **PUT** `/devices/{device_id}`  
  Update device details

- **DELETE** `/devices/{device_id}`  
  Delete a device

### Provider Routes

- **POST** `/providers/`  
  Create a new provider

- **GET** `/providers/{provider_id}`  
  Retrieve provider details

- **PUT** `/providers/{provider_id}`  
  Update provider details

- **DELETE** `/providers/{provider_id}`  
  Delete a provider

---

## Enhancing Database Relationships, Incorporating All Entities, and Optimizing Queries for Efficiency

### Current Implementation

- **Entity Relationships**:  
  - Many-to-Many between Patients and Providers  
  - One-to-Many between Patients and Devices (cascade delete enabled)

- **ORM and Schema Management**:  
  - SQLAlchemy ORM with declarative base models

- **Query Optimization**:  
  - Queries fetch, update, and delete records efficiently but can be further optimized

### Enhancements and Optimizations

- **Optimize Query Performance**:  
  - Use `joinedload()` to fetch related entities in a single query  
  - Implement indexing for frequently queried fields

- **Improve Relationship Handling**:  
  - Fine-tune cascade behavior for controlled deletions  
  - Explicit Foreign Key constraints for better integrity

- **Reduce Overhead with Asynchronous Queries**:  
  - Utilize async SQLAlchemy for handling high request loads

- **Optimize Bulk Operations**:  
  - Use batch inserts & updates instead of individual transactions

These enhancements will improve **scalability, efficiency, and maintainability** of our API. 🚀

---

## Steps I Follow to Optimize | Minimize ERD

1. **Normalization**  
   Look for duplicate fields or repeated data that could be separated out, ensuring each entity handles only its own unique attributes and associations.

2. **Refine Relationships**  
   Avoid a “crow’s nest” diagram by simplifying or merging closely related entities. Consider whether certain relationships might be more logically handled as sub-entities or joined tables.

3. **Clarify Attribute Types**  
   Each attribute should have a clear purpose, consistent data type, and proper constraints (e.g., `NOT NULL`, unique constraints) to avoid data redundancy or confusion.

---

## Introducing Object-Oriented Concepts in ERD Design

Depending on the domain and requirements, you could consider a **hybrid approach** that models **inheritance** or **composition** directly in the ERD. For example, a “User” entity could be a parent, while “Patient” or “Provider” might be specialized sub-entities.

---

## What If I Encounter a Recursive Relationship?

Sometimes an entity can relate to itself (e.g., a manager supervising an employee). Use a self-referencing foreign key and clearly document the recursion in your ERD.

---

## Handling Validation Errors

- A `422 Unprocessable Entity` error typically indicates request data does not match the expected Pydantic schema.  
- Ensure all required fields are provided with correct data types.

---

## CRUD Implementation

CRUD stands for **Create**, **Read**, **Update**, and **Delete**:

- **Create**: Adding new records  
- **Read**: Retrieving existing records  
- **Update**: Modifying records  
- **Delete**: Removing records  

Our implementation leverages SQLAlchemy for data persistence and relationship management.

---

## Notes

- If you encounter a database error or need a fresh start:

  ```bash
  rm database/database.db
  python database/create_db.py
  ```
- Always activate your virtual environment before installing dependencies or running the server.

---

## Future Implementations Would Be Good to Have

- **Authentication & Authorization** (e.g., JWT, OAuth2)  
- **Asynchronous Processing** for higher concurrency  
- **Database Migrations** (e.g., Alembic) and performance tuning  
- **Comprehensive Logging & Monitoring**  
- **Integration with FHIR or other external APIs**  
- **Frontend Integration** (e.g., React or Vue)

---

## Conclusion

In this assignment, I have:

- Built a RESTful API using **FastAPI**  
- Designed an **ERD** for **Patients**, **Devices**, and **Providers**  
- Implemented SQLAlchemy models, CRUD operations, and data validation with Pydantic  
- Gained practical experience in backend development and scalable API design

This project reinforces best practices in API design, data modeling, and application architecture.

---

## Summary

This document provides a comprehensive overview of the Assignment 02 project. It includes:

- Detailed installation and environment setup instructions.
- A clear project folder structure reflecting that the CRUD functions are within the `database` directory.
- An explanation of API endpoints for Patients, Devices, and Providers.
- Sections on enhancing database relationships, query optimizations, and ERD design considerations.
- Instructions on handling validation errors and best practices for CRUD operations.
- A conclusion summarizing the project achievements.
- Complete code implementation sections covering connection, models, database initialization, schemas, CRUD operations, and routers.

---

## Code Implementation

Below are the key code snippets for this project. Update or replace these blocks with your final implementations as needed.

---

### 1. `database/connection.py`
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# ✅ Load environment variables from .env file (if available)
load_dotenv()

# ✅ Use environment variable for DATABASE_URL (default to SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# ✅ Create Engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# ✅ Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Use DeclarativeBase (SQLAlchemy 2.0)
class Base(DeclarativeBase):
    pass

# ✅ Dependency for FastAPI: Ensures correct session management
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### 2. `database/models.py`
```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database.connection import Base  # Keeping original import

# ✅ Many-to-Many Relationship: Patient ↔ Provider
patient_provider_association = Table(
    "patient_provider_association",
    Base.metadata,
    Column("patient_id", Integer, ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True),
    Column("provider_id", Integer, ForeignKey("providers.id", ondelete="CASCADE"), primary_key=True),
)

# ✅ Provider Model
class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    specialty = Column(String, nullable=False)

    # Many-to-Many with Patients
    patients = relationship("Patient", secondary=patient_provider_association, back_populates="providers")

# ✅ Patient Model 
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)

    # ✅ Many-to-Many with Providers (Explicitly Remove on Delete)
    providers = relationship(
        "Provider",
        secondary=patient_provider_association,
        back_populates="patients",
        cascade="all, delete",  # Ensures associated records are removed
        passive_deletes=True    # Helps with foreign key constraints
    )

    # ✅ One-to-Many with Devices (Ensure Correct back_populates)
    devices = relationship(
        "Device",
        back_populates="patient",
        cascade="all, delete",
        passive_deletes=True
    )

# ✅ Device Model (One-to-Many with Patients)
class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=True)

    # ✅ Foreign Key to Patient
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    
    patient = relationship("Patient", back_populates="devices")
```

---

### 3. `database/create_db.py`
```python
import sys
import os
import sqlite3

# Ensure the script runs with the correct path settings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.connection import engine, Base
from database.models import Patient, Device, Provider, patient_provider_association  # Import all models

# Define the database file path inside the database folder
DATABASE_PATH = "database/database.db"

def create_tables():
    """Creates database tables using SQLAlchemy models."""
    print("\n🚀 Creating database tables...")
    try:
        # Drop existing tables (CAUTION: This will delete all data!)
        Base.metadata.drop_all(bind=engine)
        print("🗑️ Dropped existing tables!")

        # Create tables with updated schema
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

def verify_tables():
    """Verifies if tables exist in the SQLite database."""
    print("\n🔍 Verifying existing tables in database.db...")
    try:
        conn = sqlite3.connect(DATABASE_PATH)  # Ensure correct database path
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()

        if tables:
            print(f"✅ Existing tables: {[table[0] for table in tables]}")
        else:
            print("⚠️ No tables found. Make sure your models are properly defined.")
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")

if __name__ == "__main__":
    # Ensure database directory exists
    if not os.path.exists("database"):
        os.makedirs("database")

    # Remove old database file before recreating it
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print("🗑️ Old database file removed.")

    create_tables()
    verify_tables()
```

---

### 4. `main.py`
```python
from fastapi import FastAPI
from routers import patient_routes, device_routes, provider_routes  # Adjust imports as needed

app = FastAPI(
    title="Healthcare Management API",
    description="CRUD operations on Patients, Devices, and Providers",
    version="0.1.0",
)

# Register routers
app.include_router(patient_routes.router, prefix="/patients", tags=["Patients"])
app.include_router(device_routes.router, prefix="/devices", tags=["Devices"])
app.include_router(provider_routes.router, prefix="/providers", tags=["Providers"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Healthcare Management API!"}
```

---

### 5. `schemas/device.py`
```python
from pydantic import BaseModel
from typing import Optional

class DeviceSchema(BaseModel):
    id: int
    serial_number: str
    patient_id: Optional[int] = None  # ✅ Fix: Foreign Key
    active: bool = True

    class Config:
        from_attributes = True
```

---

### 6. `schemas/patient.py`
```python
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class DeviceSchema(BaseModel):
    id: int
    serial_number: str
    active: bool = True

class ProviderSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    specialty: Optional[str] = None

class PatientSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    active: bool = True
    devices: List[DeviceSchema] = []  # ✅ Fix: List of Device objects
    providers: List[ProviderSchema] = []  # ✅ Fix: Many-to-Many relationship

    class Config:
        from_attributes = True  # ✅ Helps SQLAlchemy models map to Pydantic
```

---

### 7. `schemas/provider.py`
```python
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class PatientSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    active: bool = True

class ProviderSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    specialty: Optional[str] = None
    patients: List[PatientSchema] = []  # ✅ Fix: Many-to-Many relationship

    class Config:
        from_attributes = True
```

---

### 8. `crud/device_crud.py`
```python
from sqlalchemy.orm import Session
from database.models import Device, Patient
from schemas.device import DeviceSchema

# ✅ Create a new device
def create_device(db: Session, device: DeviceSchema):
    new_device = Device(**device.dict())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

# ✅ Get a device by ID
def get_device(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()

# ✅ Assign a device to a patient
def assign_device_to_patient(db: Session, device_id: int, patient_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not device or not patient:
        return None

    device.patient_id = patient_id
    db.commit()
    return device

# ✅ Update an existing device (Allows reassigning Patient)
def update_device(db: Session, device_id: int, device_data: DeviceSchema):
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        return None  # Device not found

    device_dict = device_data.model_dump(exclude_unset=True)

    # ✅ Check if `patient_id` is provided and reassign the device
    if "patient_id" in device_dict:
        new_patient = db.query(Patient).filter(Patient.id == device_dict["patient_id"]).first()
        if new_patient:
            device.patient = new_patient  # Reassign device to new patient

    for key, value in device_dict.items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)
    return device

# ✅ Delete a device
def delete_device(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if device:
        db.delete(device)
        db.commit()
        return True
    return False
```

---

### 9. `crud/patient_crud.py`
```python
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import Patient, Provider, Device
from schemas.patient import PatientSchema

# ✅ Create a new patient
def create_patient(db: Session, patient: PatientSchema):
    new_patient = Patient(**patient.model_dump())  # Using .model_dump() instead of .dict()
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

# ✅ Get a patient by ID (including related providers & devices)
def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

# ✅ Assign a provider to a patient (Many-to-Many)
def assign_provider_to_patient(db: Session, patient_id: int, provider_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    
    if not patient or not provider:
        return None
    
    if provider in patient.providers:
        return patient  # Already assigned

    patient.providers.append(provider)
    db.commit()
    return patient

# ✅ Assign a device to a patient (One-to-Many)
def assign_device_to_patient(db: Session, patient_id: int, device_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    device = db.query(Device).filter(Device.id == device_id).first()

    if not patient or not device:
        return None  # Either patient or device does not exist

    if device in patient.devices:
        return patient  # Already assigned

    patient.devices.append(device)
    db.commit()
    return patient

# ✅ Update an existing patient (including assigned devices & providers)
def update_patient(db: Session, patient_id: int, patient_data: PatientSchema):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        return None  # Patient not found

    # Update patient attributes (excluding relationships)
    patient_dict = patient_data.model_dump(exclude_unset=True, exclude={"device_ids", "provider_ids"})
    for key, value in patient_dict.items():
        setattr(patient, key, value)

    # Update assigned devices if `device_ids` are provided
    if "device_ids" in patient_data.model_dump():
        new_devices = db.query(Device).filter(Device.id.in_(patient_data.device_ids)).all()
        patient.devices = new_devices

    # Update assigned providers if `provider_ids` are provided
    if "provider_ids" in patient_data.model_dump():
        new_providers = db.query(Provider).filter(Provider.id.in_(patient_data.provider_ids)).all()
        patient.providers = new_providers

    db.commit()
    db.refresh(patient)
    return patient

# ✅ Remove a provider from a patient
def remove_provider_from_patient(db: Session, patient_id: int, provider_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not patient or not provider:
        return None

    if provider in patient.providers:
        patient.providers.remove(provider)
        db.commit()
    
    return patient

# ✅ Remove a device from a patient (One-to-Many)
def remove_device_from_patient(db: Session, patient_id: int, device_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    device = db.query(Device).filter(Device.id == device_id).first()

    if not patient or not device:
        return None  # Either patient or device does not exist

    if device in patient.devices:
        patient.devices.remove(device)
        db.commit()

    return patient

def delete_patient(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Optional: Remove associations first (Many-to-Many)
    patient.providers = []
    patient.devices = []
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}
```

---

### 10. `crud/provider_crud.py`
```python
from sqlalchemy.orm import Session
from database.models import Provider, patient_provider_association
from schemas.provider import ProviderSchema

# ✅ Create a new provider
def create_provider(db: Session, provider: ProviderSchema):
    new_provider = Provider(**provider.dict())
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider

# ✅ Get a provider by ID
def get_provider(db: Session, provider_id: int):
    return db.query(Provider).filter(Provider.id == provider_id).first()

# ✅ Update an existing provider (No patient association needed)
def update_provider(db: Session, provider_id: int, provider_data: ProviderSchema):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    
    if not provider:
        return None  # Provider not found

    for key, value in provider_data.model_dump(exclude_unset=True).items():
        setattr(provider, key, value)

    db.commit()
    db.refresh(provider)
    return provider

# ✅ Delete a provider (Removes association, keeps patients)
def delete_provider(db: Session, provider_id: int):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if provider:
        db.query(patient_provider_association).filter(
            patient_provider_association.c.provider_id == provider_id
        ).delete()

        db.delete(provider)
        db.commit()
        return True
    return False

# ✅ Get all patients assigned to a provider
def get_patients_by_provider(db: Session, provider_id: int):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    return provider.patients if provider else None
```

---

### 11. `routers/device_routes.py`
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.crud.device_crud import (
    create_device, get_device, update_device, delete_device
)
from schemas.device import DeviceSchema

router = APIRouter(prefix="/devices", tags=["Devices"])

# ✅ Create a new Device
@router.post("/", response_model=DeviceSchema)
def create_device_route(device: DeviceSchema, db: Session = Depends(get_db)):
    return create_device(db, device)

# ✅ Get a Device by ID
@router.get("/{device_id}", response_model=DeviceSchema)
def get_device_route(device_id: int, db: Session = Depends(get_db)):
    device = get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

# ✅ Update a Device (Supports reassignment to another Patient)
@router.put("/{device_id}", response_model=DeviceSchema)
def update_device_route(device_id: int, device_data: DeviceSchema, db: Session = Depends(get_db)):
    updated_device = update_device(db, device_id, device_data)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device

# ✅ Delete a Device
@router.delete("/{device_id}")
def delete_device_route(device_id: int, db: Session = Depends(get_db)):
    if not delete_device(db, device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}
```

---

### 12. `routers/patient_routes.py`
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.crud.patient_crud import (
    create_patient, get_patient, update_patient, delete_patient,
    assign_provider_to_patient, remove_provider_from_patient,
    assign_device_to_patient, remove_device_from_patient
)
from schemas.patient import PatientSchema

router = APIRouter(prefix="/patients", tags=["Patients"])

# ✅ Create a new Patient
@router.post("/", response_model=PatientSchema, summary="Create Patient")
def create_patient_route(patient: PatientSchema, db: Session = Depends(get_db)):
    return create_patient(db, patient)

# ✅ Get a Patient by ID (Includes Providers & Devices)
@router.get("/{patient_id}", response_model=PatientSchema, summary="Get Patient")
def get_patient_route(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# ✅ Update a Patient
@router.put("/{patient_id}", response_model=PatientSchema)
def update_patient_route(patient_id: int, patient_data: PatientSchema, db: Session = Depends(get_db)):
    updated_patient = update_patient(db, patient_id, patient_data)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient

# ✅ Delete a Patient (Cascades to Devices & Associations)
@router.delete("/{patient_id}", summary="Delete a Patient")
def delete_patient_route(patient_id: int, db: Session = Depends(get_db)):
    if not delete_patient(db, patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}

# ✅ Assign a Provider to a Patient (Many-to-Many)
@router.post("/{patient_id}/providers/{provider_id}", summary="Assign Provider")
def assign_provider_route(patient_id: int, provider_id: int, db: Session = Depends(get_db)):
    patient = assign_provider_to_patient(db, patient_id, provider_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Provider not found")
    return patient

# ✅ Remove a Provider from a Patient
@router.delete("/{patient_id}/providers/{provider_id}")
def remove_provider_route(patient_id: int, provider_id: int, db: Session = Depends(get_db)):
    patient = remove_provider_from_patient(db, patient_id, provider_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Provider not found")
    return patient

# ✅ Assign a Device to a Patient (One-to-Many)
@router.post("/{patient_id}/devices/{device_id}")
def assign_device_route(patient_id: int, device_id: int, db: Session = Depends(get_db)):
    patient = assign_device_to_patient(db, patient_id, device_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Device not found")
    return patient

# ✅ Remove a Device from a Patient
@router.delete("/{patient_id}/devices/{device_id}")
def remove_device_route(patient_id: int, device_id: int, db: Session = Depends(get_db)):
    patient = remove_device_from_patient(db, patient_id, device_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Device not found")
    return patient
```

---

### 13. `routers/provider_routes.py`
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.crud.provider_crud import (
    create_provider, get_provider, update_provider, delete_provider, get_patients_by_provider
)
from schemas.provider import ProviderSchema

router = APIRouter(prefix="/providers", tags=["Providers"])

# ✅ Create a new Provider
@router.post("/", response_model=ProviderSchema)
def create_provider_route(provider: ProviderSchema, db: Session = Depends(get_db)):
    return create_provider(db, provider)

# ✅ Get a Provider by ID
@router.get("/{provider_id}", response_model=ProviderSchema)
def get_provider_route(provider_id: int, db: Session = Depends(get_db)):
    provider = get_provider(db, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

# ✅ Update a Provider
@router.put("/{provider_id}", response_model=ProviderSchema)
def update_provider_route(provider_id: int, provider_data: ProviderSchema, db: Session = Depends(get_db)):
    updated_provider = update_provider(db, provider_id, provider_data)
    if not updated_provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return updated_provider

# ✅ Delete a Provider (Only removes association, keeps Patients)
@router.delete("/{provider_id}")
def delete_provider_route(provider_id: int, db: Session = Depends(get_db)):
    if not delete_provider(db, provider_id):
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Provider deleted successfully"}

# ✅ Get all Patients assigned to a Provider
@router.get("/{provider_id}/patients")
def get_patients(provider_id: int, db: Session = Depends(get_db)):
    patients = get_patients_by_provider(db, provider_id)
    if not patients:
        raise HTTPException(status_code=404, detail="No patients found for this provider")
    return patients
```

---

## Summary

This Markdown document provides a comprehensive guide for Assignment 02: From Specification to API. It includes:

- **Installation & Setup Instructions:** Steps to clone the repository, set up a virtual environment, install dependencies, and run the API server.
- **Environment Configuration:** Details on setting up a `.env` file for environment variables.
- **Project Folder Structure:** A detailed outline of the project directories, including the `crud` folder within the `database` directory.
- **API Endpoints:** An overview of the API endpoints for Patient, Device, and Provider routes.
- **Enhancements and Optimizations:** Information on the current implementation and potential improvements for query performance, relationship handling, and overall efficiency.
- **Steps to Optimize / Minimize ERD:** Strategies for normalization, refining relationships, and clarifying attribute types.
- **Object-Oriented Concepts in ERD Design:** A discussion on employing inheritance or composition in the ERD.
- **Handling Recursive Relationships and Validation Errors:** Guidelines on managing self-referencing keys and ensuring proper data validation.
- **CRUD Implementation:** Details on how CRUD operations are implemented using SQLAlchemy.
- **Code Implementation:** Complete code snippets for connection, models, database initialization, schemas, CRUD operations, and routers.
- **Conclusion:** A summary of the project achievements and lessons learned.

---

## Conclusion

In this assignment, I have:

- Built a RESTful API using **FastAPI**  
- Designed an **ERD** for **Patients**, **Devices**, and **Providers**  
- Implemented SQLAlchemy models, CRUD operations, and data validation with Pydantic  
- Gained practical experience in backend development and scalable API design

This project reinforces best practices in API design, data modeling, and application architecture.

---

## Code Implementation

Below are the key code snippets for this project. Update or replace these blocks with your final implementations as needed.

### 1. `database/connection.py`
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# ✅ Load environment variables from .env file (if available)
load_dotenv()

# ✅ Use environment variable for DATABASE_URL (default to SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# ✅ Create Engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# ✅ Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Use DeclarativeBase (SQLAlchemy 2.0)
class Base(DeclarativeBase):
    pass

# ✅ Dependency for FastAPI: Ensures correct session management
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### 2. `database/models.py`
```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database.connection import Base  # Keeping original import

# ✅ Many-to-Many Relationship: Patient ↔ Provider
patient_provider_association = Table(
    "patient_provider_association",
    Base.metadata,
    Column("patient_id", Integer, ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True),
    Column("provider_id", Integer, ForeignKey("providers.id", ondelete="CASCADE"), primary_key=True),
)

# ✅ Provider Model
class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    specialty = Column(String, nullable=False)

    # Many-to-Many with Patients
    patients = relationship("Patient", secondary=patient_provider_association, back_populates="providers")

# ✅ Patient Model 
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)

    # ✅ Many-to-Many with Providers (Explicitly Remove on Delete)
    providers = relationship(
        "Provider",
        secondary=patient_provider_association,
        back_populates="patients",
        cascade="all, delete",  # Ensures associated records are removed
        passive_deletes=True    # Helps with foreign key constraints
    )

    # ✅ One-to-Many with Devices (Ensure Correct back_populates)
    devices = relationship(
        "Device",
        back_populates="patient",
        cascade="all, delete",
        passive_deletes=True
    )

# ✅ Device Model (One-to-Many with Patients)
class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=True)

    # ✅ Foreign Key to Patient
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    
    patient = relationship("Patient", back_populates="devices")
```

---

### 3. `database/create_db.py`
```python
import sys
import os
import sqlite3

# Ensure the script runs with the correct path settings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.connection import engine, Base
from database.models import Patient, Device, Provider, patient_provider_association  # Import all models

# Define the database file path inside the database folder
DATABASE_PATH = "database/database.db"

def create_tables():
    """Creates database tables using SQLAlchemy models."""
    print("\n🚀 Creating database tables...")
    try:
        # Drop existing tables (CAUTION: This will delete all data!)
        Base.metadata.drop_all(bind=engine)
        print("🗑️ Dropped existing tables!")

        # Create tables with updated schema
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

def verify_tables():
    """Verifies if tables exist in the SQLite database."""
    print("\n🔍 Verifying existing tables in database.db...")
    try:
        conn = sqlite3.connect(DATABASE_PATH)  # Ensure correct database path
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()

        if tables:
            print(f"✅ Existing tables: {[table[0] for table in tables]}")
        else:
            print("⚠️ No tables found. Make sure your models are properly defined.")
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")

if __name__ == "__main__":
    # Ensure database directory exists
    if not os.path.exists("database"):
        os.makedirs("database")

    # Remove old database file before recreating it
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print("🗑️ Old database file removed.")

    create_tables()
    verify_tables()
```

---

### 4. `main.py`
```python
from fastapi import FastAPI
from routers import patient_routes, device_routes, provider_routes  # Adjust imports as needed

app = FastAPI(
    title="Healthcare Management API",
    description="CRUD operations on Patients, Devices, and Providers",
    version="0.1.0",
)

# Register routers
app.include_router(patient_routes.router, prefix="/patients", tags=["Patients"])
app.include_router(device_routes.router, prefix="/devices", tags=["Devices"])
app.include_router(provider_routes.router, prefix="/providers", tags=["Providers"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Healthcare Management API!"}
```

---

### 5. `schemas/device.py`
```python
from pydantic import BaseModel
from typing import Optional

class DeviceSchema(BaseModel):
    id: int
    serial_number: str
    patient_id: Optional[int] = None  # ✅ Fix: Foreign Key
    active: bool = True

    class Config:
        from_attributes = True
```

---

### 6. `schemas/patient.py`
```python
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class DeviceSchema(BaseModel):
    id: int
    serial_number: str
    active: bool = True

class ProviderSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    specialty: Optional[str] = None

class PatientSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    active: bool = True
    devices: List[DeviceSchema] = []  # ✅ Fix: List of Device objects
    providers: List[ProviderSchema] = []  # ✅ Fix: Many-to-Many relationship

    class Config:
        from_attributes = True  # ✅ Helps SQLAlchemy models map to Pydantic
```

---

### 7. `schemas/provider.py`
```python
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class PatientSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    active: bool = True

class ProviderSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    specialty: Optional[str] = None
    patients: List[PatientSchema] = []  # ✅ Fix: Many-to-Many relationship

    class Config:
        from_attributes = True
```

---

### 8. `crud/device_crud.py`
```python
from sqlalchemy.orm import Session
from database.models import Device, Patient
from schemas.device import DeviceSchema

# ✅ Create a new device
def create_device(db: Session, device: DeviceSchema):
    new_device = Device(**device.dict())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

# ✅ Get a device by ID
def get_device(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()

# ✅ Assign a device to a patient
def assign_device_to_patient(db: Session, device_id: int, patient_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not device or not patient:
        return None

    device.patient_id = patient_id
    db.commit()
    return device

# ✅ Update an existing device (Allows reassigning Patient)
def update_device(db: Session, device_id: int, device_data: DeviceSchema):
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        return None  # Device not found

    device_dict = device_data.model_dump(exclude_unset=True)

    # ✅ Check if `patient_id` is provided and reassign the device
    if "patient_id" in device_dict:
        new_patient = db.query(Patient).filter(Patient.id == device_dict["patient_id"]).first()
        if new_patient:
            device.patient = new_patient  # Reassign device to new patient

    for key, value in device_dict.items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)
    return device

# ✅ Delete a device
def delete_device(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if device:
        db.delete(device)
        db.commit()
        return True
    return False
```

---

### 9. `crud/patient_crud.py`
```python
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import Patient, Provider, Device
from schemas.patient import PatientSchema

# ✅ Create a new patient
def create_patient(db: Session, patient: PatientSchema):
    new_patient = Patient(**patient.model_dump())  # Using .model_dump() instead of .dict()
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

# ✅ Get a patient by ID (including related providers & devices)
def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

# ✅ Assign a provider to a patient (Many-to-Many)
def assign_provider_to_patient(db: Session, patient_id: int, provider_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    
    if not patient or not provider:
        return None
    
    if provider in patient.providers:
        return patient  # Already assigned

    patient.providers.append(provider)
    db.commit()
    return patient

# ✅ Assign a device to a patient (One-to-Many)
def assign_device_to_patient(db: Session, patient_id: int, device_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    device = db.query(Device).filter(Device.id == device_id).first()

    if not patient or not device:
        return None  # Either patient or device does not exist

    if device in patient.devices:
        return patient  # Already assigned

    patient.devices.append(device)
    db.commit()
    return patient

# ✅ Update an existing patient (including assigned devices & providers)
def update_patient(db: Session, patient_id: int, patient_data: PatientSchema):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        return None  # Patient not found

    # Update patient attributes (excluding relationships)
    patient_dict = patient_data.model_dump(exclude_unset=True, exclude={"device_ids", "provider_ids"})
    for key, value in patient_dict.items():
        setattr(patient, key, value)

    # Update assigned devices if `device_ids` are provided
    if "device_ids" in patient_data.model_dump():
        new_devices = db.query(Device).filter(Device.id.in_(patient_data.device_ids)).all()
        patient.devices = new_devices

    # Update assigned providers if `provider_ids` are provided
    if "provider_ids" in patient_data.model_dump():
        new_providers = db.query(Provider).filter(Provider.id.in_(patient_data.provider_ids)).all()
        patient.providers = new_providers

    db.commit()
    db.refresh(patient)
    return patient

# ✅ Remove a provider from a patient
def remove_provider_from_patient(db: Session, patient_id: int, provider_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not patient or not provider:
        return None

    if provider in patient.providers:
        patient.providers.remove(provider)
        db.commit()
    
    return patient

# ✅ Remove a device from a patient (One-to-Many)
def remove_device_from_patient(db: Session, patient_id: int, device_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    device = db.query(Device).filter(Device.id == device_id).first()

    if not patient or not device:
        return None  # Either patient or device does not exist

    if device in patient.devices:
        patient.devices.remove(device)
        db.commit()

    return patient

def delete_patient(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Optional: Remove associations first (Many-to-Many)
    patient.providers = []
    patient.devices = []
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}
```

---

### 10. `crud/provider_crud.py`
```python
from sqlalchemy.orm import Session
from database.models import Provider, patient_provider_association
from schemas.provider import ProviderSchema

# ✅ Create a new provider
def create_provider(db: Session, provider: ProviderSchema):
    new_provider = Provider(**provider.dict())
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider

# ✅ Get a provider by ID
def get_provider(db: Session, provider_id: int):
    return db.query(Provider).filter(Provider.id == provider_id).first()

# ✅ Update an existing provider (No patient association needed)
def update_provider(db: Session, provider_id: int, provider_data: ProviderSchema):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    
    if not provider:
        return None  # Provider not found

    for key, value in provider_data.model_dump(exclude_unset=True).items():
        setattr(provider, key, value)

    db.commit()
    db.refresh(provider)
    return provider

# ✅ Delete a provider (Removes association, keeps patients)
def delete_provider(db: Session, provider_id: int):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if provider:
        db.query(patient_provider_association).filter(
            patient_provider_association.c.provider_id == provider_id
        ).delete()

        db.delete(provider)
        db.commit()
        return True
    return False

# ✅ Get all patients assigned to a provider
def get_patients_by_provider(db: Session, provider_id: int):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    return provider.patients if provider else None
```

---

### 11. `routers/device_routes.py`
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.crud.device_crud import (
    create_device, get_device, update_device, delete_device
)
from schemas.device import DeviceSchema

router = APIRouter(prefix="/devices", tags=["Devices"])

# ✅ Create a new Device
@router.post("/", response_model=DeviceSchema)
def create_device_route(device: DeviceSchema, db: Session = Depends(get_db)):
    return create_device(db, device)

# ✅ Get a Device by ID
@router.get("/{device_id}", response_model=DeviceSchema)
def get_device_route(device_id: int, db: Session = Depends(get_db)):
    device = get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

# ✅ Update a Device (Supports reassignment to another Patient)
@router.put("/{device_id}", response_model=DeviceSchema)
def update_device_route(device_id: int, device_data: DeviceSchema, db: Session = Depends(get_db)):
    updated_device = update_device(db, device_id, device_data)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device

# ✅ Delete a Device
@router.delete("/{device_id}")
def delete_device_route(device_id: int, db: Session = Depends(get_db)):
    if not delete_device(db, device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}
```

---

### 12. `routers/patient_routes.py`
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.crud.patient_crud import (
    create_patient, get_patient, update_patient, delete_patient,
    assign_provider_to_patient, remove_provider_from_patient,
    assign_device_to_patient, remove_device_from_patient
)
from schemas.patient import PatientSchema

router = APIRouter(prefix="/patients", tags=["Patients"])

# ✅ Create a new Patient
@router.post("/", response_model=PatientSchema, summary="Create Patient")
def create_patient_route(patient: PatientSchema, db: Session = Depends(get_db)):
    return create_patient(db, patient)

# ✅ Get a Patient by ID (Includes Providers & Devices)
@router.get("/{patient_id}", response_model=PatientSchema, summary="Get Patient")
def get_patient_route(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# ✅ Update a Patient
@router.put("/{patient_id}", response_model=PatientSchema)
def update_patient_route(patient_id: int, patient_data: PatientSchema, db: Session = Depends(get_db)):
    updated_patient = update_patient(db, patient_id, patient_data)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient

# ✅ Delete a Patient (Cascades to Devices & Associations)
@router.delete("/{patient_id}", summary="Delete a Patient")
def delete_patient_route(patient_id: int, db: Session = Depends(get_db)):
    if not delete_patient(db, patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}

# ✅ Assign a Provider to a Patient (Many-to-Many)
@router.post("/{patient_id}/providers/{provider_id}", summary="Assign Provider")
def assign_provider_route(patient_id: int, provider_id: int, db: Session = Depends(get_db)):
    patient = assign_provider_to_patient(db, patient_id, provider_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Provider not found")
    return patient

# ✅ Remove a Provider from a Patient
@router.delete("/{patient_id}/providers/{provider_id}")
def remove_provider_route(patient_id: int, provider_id: int, db: Session = Depends(get_db)):
    patient = remove_provider_from_patient(db, patient_id, provider_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Provider not found")
    return patient

# ✅ Assign a Device to a Patient (One-to-Many)
@router.post("/{patient_id}/devices/{device_id}")
def assign_device_route(patient_id: int, device_id: int, db: Session = Depends(get_db)):
    patient = assign_device_to_patient(db, patient_id, device_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Device not found")
    return patient

# ✅ Remove a Device from a Patient
@router.delete("/{patient_id}/devices/{device_id}")
def remove_device_route(patient_id: int, device_id: int, db: Session = Depends(get_db)):
    patient = remove_device_from_patient(db, patient_id, device_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient or Device not found")
    return patient
```

---

### 13. `routers/provider_routes.py`
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.crud.provider_crud import (
    create_provider, get_provider, update_provider, delete_provider, get_patients_by_provider
)
from schemas.provider import ProviderSchema

router = APIRouter(prefix="/providers", tags=["Providers"])

# ✅ Create a new Provider
@router.post("/", response_model=ProviderSchema)
def create_provider_route(provider: ProviderSchema, db: Session = Depends(get_db)):
    return create_provider(db, provider)

# ✅ Get a Provider by ID
@router.get("/{provider_id}", response_model=ProviderSchema)
def get_provider_route(provider_id: int, db: Session = Depends(get_db)):
    provider = get_provider(db, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

# ✅ Update a Provider
@router.put("/{provider_id}", response_model=ProviderSchema)
def update_provider_route(provider_id: int, provider_data: ProviderSchema, db: Session = Depends(get_db)):
    updated_provider = update_provider(db, provider_id, provider_data)
    if not updated_provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return updated_provider

# ✅ Delete a Provider (Only removes association, keeps Patients)
@router.delete("/{provider_id}")
def delete_provider_route(provider_id: int, db: Session = Depends(get_db)):
    if not delete_provider(db, provider_id):
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Provider deleted successfully"}

# ✅ Get all Patients assigned to a Provider
@router.get("/{provider_id}/patients")
def get_patients(provider_id: int, db: Session = Depends(get_db)):
    patients = get_patients_by_provider(db, provider_id)
    if not patients:
        raise HTTPException(status_code=404, detail="No patients found for this provider")
    return patients
```

---

**End of Document**

This updated Markdown document now includes:

- A collapsible, clickable Table of Contents.
- Updated folder structure indicating the `crud` folder resides inside the `database` directory.
- A comprehensive "Conclusion" and a new "Summary" section that outlines the contents of the document.
- All the code snippets for connection, models, database initialization, schemas, CRUD operations, and routers.

Feel free to review and adjust any details as needed.
```
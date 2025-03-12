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

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    age: int
    active: bool = True
    providers: List["Provider"] = Relationship(back_populates="patients")
    devices: List["Device"] = Relationship(back_populates="patient")
```
#### **How It Meets Assignment Requirements:**
- **Enforces unique emails** for patients.
- **Supports relationships with providers & devices.**
- **Ensures compatibility across different repositories.**

### **🔹 Provider Model (`database/models.py`)**
```python
class Provider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    specialty: str
    patients: List[Patient] = Relationship(back_populates="providers")
```
#### **Why It’s Important:**
- **Defines provider-patient relationships.**
- **Ensures unique provider emails.**
- **Allows seamless CRUD operations across repositories.**

### **🔹 Device Model (`database/models.py`)**
```python
class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    patient_id: Optional[int] = Field(default=None, foreign_key="patient.id")
    patient: Optional[Patient] = Relationship(back_populates="devices")
```
#### **Key Features:**
- **Links devices to patients** using `patient_id`.
- **Allows tracking of medical devices assigned to patients.**
- **Enforces referential integrity.**

---

## **2. CRUD Operations (`database/crud/`)**
Each entity (Patient, Provider, Device) has its own **CRUD operations** implemented in separate files.

### **🔹 Patient CRUD (`database/crud/patient_crud.py`)**
```python
from sqlmodel import Session
from database.models import Patient

def create_patient(db: Session, patient_data):
    patient = Patient(**patient_data.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)
    if patient:
        db.delete(patient)
        db.commit()
        return True
    return False
```
#### **How It Supports the Assignment:**
- **Abstracts data persistence using CRUD functions.**
- **Allows flexible storage backend switching via repositories.**

### **🔹 Provider CRUD (`database/crud/provider_crud.py`)**
```python
from sqlmodel import Session
from database.models import Provider

def create_provider(db: Session, provider_data):
    provider = Provider(**provider_data.dict())
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider

def get_provider(db: Session, provider_id: int):
    return db.query(Provider).filter(Provider.id == provider_id).first()
```
#### **Key Features:**
- **Encapsulates database logic for providers.**
- **Enhances modularity and maintainability.**

### **🔹 Device CRUD (`database/crud/device_crud.py`)**
```python
from sqlmodel import Session
from database.models import Device

def create_device(db: Session, device_data):
    device = Device(**device_data.dict())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device
```
#### **Why It’s Needed:**
- **Manages medical devices assigned to patients.**
- **Supports scalable API endpoints.**

---

## **3. Database Initialization (`database/connection.py`)**
This module handles database connection and session management.

```python
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/database.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
```
#### **How It Meets Assignment Requirements:**
- **Creates a database connection for repositories.**
- **Supports switching between different databases using `DATABASE_URL`.**

---

## **Conclusion**
- The **database models** provide the core structure for Patient, Provider, and Device entities.
- **CRUD functions** ensure data management across repositories.
- **The repository pattern** abstracts data access, ensuring **API flexibility** across multiple storage options.
- **SQLModel ORM** provides seamless database interactions while maintaining **Pydantic validation.**

This documentation serves as a reference for managing database operations within the **FastAPI Repository Pattern**. 🚀


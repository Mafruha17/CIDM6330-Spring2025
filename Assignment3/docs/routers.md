# **Routers Documentation**

## **Overview**
This document provides an overview of the **FastAPI routers** implemented in **Assignment 03**. These routers define the API endpoints for managing **Patients, Providers, and Devices**, ensuring clean separation of concerns while interacting with the **Repository Pattern**.

Each router module corresponds to an entity and follows **dependency injection** using `Depends(get_db)`, allowing seamless integration with multiple repository types (**SQLModel, CSV, In-Memory**).

---

## **Table of Contents**
1. [Patient Router](## todo)
2. [Provider Router](#provider-router)
3. [Device Router](#device-router)
---
## **1. Patient Router (`routers/patient_routes.py`)**
This router handles **CRUD operations** for **patients**, enabling interaction with different repositories via **dependency injection**.

### **✅ Endpoints Defined**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.connection import get_db
from schemas.patient import PatientSchema
from repositories.patient_repository import PatientRepository

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/")
def create_patient_route(patient: PatientSchema, db: Session = Depends(get_db)):
    return PatientRepository(db).create(patient)

@router.get("/{patient_id}")
def get_patient_route(patient_id: int, db: Session = Depends(get_db)):
    patient = PatientRepository(db).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{patient_id}")
def update_patient_route(patient_id: int, patient_data: PatientSchema, db: Session = Depends(get_db)):
    return PatientRepository(db).update(patient_id, patient_data)

@router.delete("/{patient_id}")
def delete_patient_route(patient_id: int, db: Session = Depends(get_db)):
    success = PatientRepository(db).delete(patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}
```

### **🔹 Key Features**
- **Supports all CRUD operations** (`create`, `get`, `update`, `delete`).
- **Uses dependency injection** for seamless repository switching.
- **Implements proper exception handling** (`HTTP 404` for missing records).

---

## **2. Provider Router (`routers/provider_routes.py`)**
This router manages **CRUD operations** for **providers**, allowing interaction with different repositories.

### **✅ Endpoints Defined**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.connection import get_db
from schemas.provider import ProviderSchema
from repositories.provider_repository import ProviderRepository

router = APIRouter(prefix="/providers", tags=["Providers"])

@router.post("/")
def create_provider_route(provider: ProviderSchema, db: Session = Depends(get_db)):
    return ProviderRepository(db).create(provider)

@router.get("/{provider_id}")
def get_provider_route(provider_id: int, db: Session = Depends(get_db)):
    provider = ProviderRepository(db).get(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

@router.put("/{provider_id}")
def update_provider_route(provider_id: int, provider_data: ProviderSchema, db: Session = Depends(get_db)):
    return ProviderRepository(db).update(provider_id, provider_data)

@router.delete("/{provider_id}")
def delete_provider_route(provider_id: int, db: Session = Depends(get_db)):
    success = ProviderRepository(db).delete(provider_id)
    if not success:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Provider deleted successfully"}
```

### **🔹 Key Features**
- **CRUD operations for providers** (`create`, `get`, `update`, `delete`).
- **Ensures seamless switching between repositories.**
- **Uses dependency injection with `Depends(get_db)`.**
- **Handles missing records with proper `HTTP 404` exceptions.**

---

## **3. Device Router (`routers/device_routes.py`)**
This router manages **CRUD operations** for **medical devices**, linking them to patients.

### **✅ Endpoints Defined**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.connection import get_db
from schemas.device import DeviceSchema
from repositories.device_repository import DeviceRepository

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/")
def create_device_route(device: DeviceSchema, db: Session = Depends(get_db)):
    return DeviceRepository(db).create(device)

@router.get("/{device_id}")
def get_device_route(device_id: int, db: Session = Depends(get_db)):
    device = DeviceRepository(db).get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}")
def update_device_route(device_id: int, device_data: DeviceSchema, db: Session = Depends(get_db)):
    return DeviceRepository(db).update(device_id, device_data)

@router.delete("/{device_id}")
def delete_device_route(device_id: int, db: Session = Depends(get_db)):
    success = DeviceRepository(db).delete(device_id)
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}
```

### **🔹 Key Features**
- **CRUD operations for devices** (`create`, `get`, `update`, `delete`).
- **Supports linking devices to patients.**
- **Implements proper exception handling (`HTTP 404`).**

---

## **Conclusion**
- **Router modules** define RESTful API endpoints for Patients, Providers, and Devices.
- **Uses dependency injection** to dynamically use SQLModel, CSV, or In-Memory repositories.
- **Implements exception handling** to return meaningful API responses.
- **Provides structured API access** while keeping business logic separate in repositories.

These routers ensure that the FastAPI application follows clean architecture principles, making it modular, scalable, and easy to maintain. 🚀


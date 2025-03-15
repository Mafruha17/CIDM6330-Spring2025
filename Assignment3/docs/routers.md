# **Routers Documentation**

## **Overview**
This document provides an overview of the **FastAPI routers** implemented in **Assignment 03**. These routers define the API endpoints for managing **Patients, Providers, and Devices**, ensuring clean separation of concerns while interacting with the **Repository Pattern**.

Each router module corresponds to an entity and follows **dependency injection** using `Depends(get_db)`, allowing seamless integration with multiple repository types (**SQLModel, CSV, In-Memory**).

---

## **Table of Contents**
1. [Patient Router](#patient-router)
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
from database.crud.patient_crud import (
    create_patient, get_patient, get_all_patients, update_patient, delete_patient
)

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/", response_model=List[PatientSchema], summary="Retrieve all patients")
def read_patients(db: Session = Depends(get_db)):
    """Fetch all patients from the database."""
    return get_all_patients(db)

@router.post("/", response_model=PatientSchema, summary="Create a new patient")
def create_patient_route(patient: PatientSchema, db: Session = Depends(get_db)):
    """Create a new patient in the database."""
    return create_patient(db, patient)

@router.get("/{patient_id}", response_model=PatientSchema, summary="Retrieve a patient by ID")
def get_patient_route(patient_id: int, db: Session = Depends(get_db)):
    """Fetch a single patient by ID."""
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{patient_id}", response_model=PatientSchema, summary="Update an existing patient")
def update_patient_route(patient_id: int, patient_data: PatientSchema, db: Session = Depends(get_db)):
    """Update patient details."""
    return update_patient(db, patient_id, patient_data)

@router.delete("/{patient_id}", summary="Delete a patient")
def delete_patient_route(patient_id: int, db: Session = Depends(get_db)):
    """Delete a patient from the database."""
    success = delete_patient(db, patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Deleted"}
```

---

## **2. Provider Router (`routers/provider_routes.py`)**
This router manages **CRUD operations** for **providers**, allowing interaction with different repositories.

### **✅ Endpoints Defined**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.connection import get_db
from schemas.provider import ProviderSchema
from database.crud.provider_crud import (
    create_provider, get_provider, get_all_providers, update_provider, delete_provider,
    get_patients_by_provider
)

router = APIRouter(prefix="/providers", tags=["Providers"])

@router.post("/", response_model=ProviderSchema, summary="Create a new provider")
def create_provider_route(provider: ProviderSchema, db: Session = Depends(get_db)):
    """Create a new provider using provider schema."""
    return create_provider(db, provider.model_dump())

@router.get("/{provider_id}", response_model=ProviderSchema, summary="Get a provider by ID")
def get_provider_route(provider_id: int, db: Session = Depends(get_db)):
    """Retrieve a provider by ID."""
    return get_provider(db, provider_id)

@router.get("/", response_model=List[ProviderSchema], summary="Get all providers")
def get_all_providers_route(db: Session = Depends(get_db)):
    """Retrieve all providers."""
    return get_all_providers(db)
```

---

## **3. Device Router (`routers/device_routes.py`)**
This router manages **CRUD operations** for **medical devices**, linking them to patients.

### **✅ Endpoints Defined**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.connection import get_db
from schemas.device import DeviceSchema
from database.crud.device_crud import (
    create_device, get_device, get_all_devices, update_device, delete_device,
    assign_device_to_patient, remove_device_from_patient
)

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/", response_model=DeviceSchema, summary="Create a new device")
def create_device_route(device: DeviceSchema, db: Session = Depends(get_db)):
    """Create a new device."""
    return create_device(db, device)

@router.get("/{device_id}", response_model=DeviceSchema, summary="Get a device by ID")
def get_device_route(device_id: int, db: Session = Depends(get_db)):
    """Retrieve a device by ID."""
    return get_device(db, device_id)
```
---

## **Conclusion**
- **Router modules** define RESTful API endpoints for Patients, Providers, and Devices.
- **Uses dependency injection** to dynamically use SQLModel, CSV, or In-Memory repositories.
- **Implements exception handling** to return meaningful API responses.
- **Provides structured API access** while keeping business logic separate in repositories.

These routers ensure that the FastAPI application follows clean architecture principles, making it modular, scalable, and easy to maintain. 🚀


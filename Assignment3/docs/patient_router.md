# **Patient Router Documentation**

## **Overview**
The **Patient Router** handles all API endpoints related to **patients**. It defines RESTful routes that interact with the **Patient Repository**, ensuring **separation of concerns** and **clean architecture**.

This router follows **FastAPI’s dependency injection** model, allowing seamless integration with different data storage backends (**SQLModel, CSV, In-Memory**).

---

## **Implementation Details**
The router is implemented in **`routers/patient_routes.py`** and defines the endpoints for **creating, retrieving, updating, and deleting patients**.

### **✅ Patient Router Code (`patient_routes.py`)**
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

---

## **Key Features**
- **Implements RESTful CRUD operations** for patient management.
- **Uses `Depends(get_db)` for dependency injection** to manage database sessions.
- **Exception handling** for missing records using `HTTPException`.
- **Follows the Repository Pattern**, keeping persistence logic separate.

---

## **Usage in FastAPI**
The **Patient Router** is registered in `main.py`:
```python
from routers import patient_routes
app.include_router(patient_routes.router)
```

---

## **Conclusion**
The **Patient Router** provides a **structured, scalable, and maintainable** approach to handling patient-related API operations. By leveraging **FastAPI’s dependency injection** and **Repository Pattern**, it ensures flexibility across different storage backends.


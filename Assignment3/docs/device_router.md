# **Device Router Documentation**

## **Overview**
The **Device Router** handles all API endpoints related to **medical devices**. It defines RESTful routes that interact with the **Device Repository**, ensuring **separation of concerns** and **clean API architecture**.

This router follows **FastAPI’s dependency injection** model, allowing seamless switching between different data storage backends (**SQLModel, CSV, In-Memory**).

---

## **Implementation Details**
The router is implemented in **`routers/device_routes.py`** and provides endpoints for **creating, retrieving, updating, and deleting devices**.

### **✅ Device Router Code (`device_routes.py`)**
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

---

## **Key Features**
- **Implements RESTful CRUD operations** for device management.
- **Uses `Depends(get_db)` for dependency injection** to manage database sessions.
- **Handles exceptions** for missing devices with `HTTPException`.
- **Follows the Repository Pattern**, ensuring **API flexibility**.

---

## **Usage in FastAPI**
The **Device Router** is registered in `main.py`:
```python
from routers import device_routes
app.include_router(device_routes.router)
```

---

## **Conclusion**
The **Device Router** ensures a **structured, maintainable, and scalable** API for managing medical devices. By leveraging **FastAPI’s dependency injection** and **Repository Pattern**, it enables seamless integration with different storage backends.


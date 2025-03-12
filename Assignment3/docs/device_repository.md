# **Device Repository Documentation**

## **Overview**
The **Device Repository** is responsible for managing CRUD operations related to medical devices. It abstracts database operations and allows seamless integration with **SQLModel, CSV, and In-Memory storage** by following the **Repository Pattern**.

This repository ensures **efficient data persistence**, **validation**, and **relationships with patients** in the API.

---

## **Implementation Details**
The repository is implemented in **`repositories/device_repository.py`** and extends the **Base Repository**.

### **✅ Device Repository Code (`device_repository.py`)**
```python
from sqlmodel import Session, select
from schemas.device import DeviceSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List, Type
from database.models import Device

class DeviceRepository(BaseRepository[Device, DeviceSchema]):  
    def __init__(self, db: Session):
        super().__init__(db, Device)  

    def create(self, obj_in: DeviceSchema) -> Optional[Device]:
        obj_data = obj_in.dict(exclude_unset=True)
        obj = Device(**obj_data)  
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, device_id: int) -> Optional[Device]:
        statement = select(Device).where(Device.id == device_id)
        return self.db.exec(statement).first()

    def get_all(self) -> List[Device]:
        statement = select(Device)
        return self.db.exec(statement).all()

    def update(self, device_id: int, obj_in: DeviceSchema) -> Optional[Device]:
        obj = self.get(device_id)
        if not obj:
            return None
        update_data = obj_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, device_id: int) -> bool:
        obj = self.get(device_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
```

---

## **Key Features**
- **Encapsulates all CRUD operations for devices.**
- **Follows the Repository Pattern for structured data management.**
- **Supports multiple storage backends (SQL, CSV, In-Memory).**
- **Ensures compatibility with FastAPI’s dependency injection system.**

---

## **Usage in FastAPI Routes**
The **Device Repository** is utilized in `device_routes.py` as follows:

```python
@router.post("/")
def create_device_route(device: DeviceSchema, db: Session = Depends(get_db)):
    return DeviceRepository(db).create(device)
```

---

## **Conclusion**
The **Device Repository** ensures an **efficient, scalable, and modular** approach to device management. It provides **data consistency** and **flexibility** across different storage backends, allowing for a highly adaptable system architecture.


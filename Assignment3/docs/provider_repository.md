# **Provider Repository Documentation**

## **Overview**
The **Provider Repository** handles CRUD operations related to healthcare providers. It abstracts the database interactions and enables seamless switching between **SQLModel, CSV, and In-Memory storage** through the **Repository Pattern**.

This repository ensures **data persistence**, **validation**, and **scalability** for provider-related operations in the API.

---

## **Implementation Details**
The repository is implemented in **`repositories/provider_repository.py`** and extends the **Base Repository**.

### **✅ Provider Repository Code (`provider_repository.py`)**
```python
from sqlmodel import Session, select
from schemas.provider import ProviderSchema
from repositories.base_repository import BaseRepository
from typing import Optional, List, Type
from database.models import Provider

class ProviderRepository(BaseRepository[Provider, ProviderSchema]):  
    def __init__(self, db: Session):
        super().__init__(db, Provider)  

    def create(self, obj_in: ProviderSchema) -> Optional[Provider]:
        obj_data = obj_in.dict(exclude_unset=True)
        obj = Provider(**obj_data)  
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, provider_id: int) -> Optional[Provider]:
        statement = select(Provider).where(Provider.id == provider_id)
        return self.db.exec(statement).first()

    def get_all(self) -> List[Provider]:
        statement = select(Provider)
        return self.db.exec(statement).all()

    def update(self, provider_id: int, obj_in: ProviderSchema) -> Optional[Provider]:
        obj = self.get(provider_id)
        if not obj:
            return None
        update_data = obj_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, provider_id: int) -> bool:
        obj = self.get(provider_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
```

---

## **Key Features**
- **Encapsulates all CRUD operations for providers.**
- **Follows the Repository Pattern for clean data management.**
- **Supports multiple storage backends (SQL, CSV, In-Memory).**
- **Ensures compatibility with FastAPI's dependency injection.**

---

## **Usage in FastAPI Routes**
The **Provider Repository** is integrated into `provider_routes.py` as follows:

```python
@router.post("/")
def create_provider_route(provider: ProviderSchema, db: Session = Depends(get_db)):
    return ProviderRepository(db).create(provider)
```

---

## **Conclusion**
The **Provider Repository** ensures a **modular, scalable, and efficient** data management system for provider-related operations. By using the **Repository Pattern**, it provides a clean abstraction over different storage methods while maintaining **data consistency and API flexibility**.


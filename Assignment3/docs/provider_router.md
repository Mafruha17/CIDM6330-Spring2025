# **Provider Router Documentation**

## **Overview**
The **Provider Router** handles all API endpoints related to **providers**. It defines RESTful routes that interact with the **Provider Repository**, ensuring a **clean separation of concerns** between API routes and database logic.

This router follows **FastAPI’s dependency injection** model, allowing seamless switching between different data storage backends (**SQLModel, CSV, In-Memory**).

---

## **Implementation Details**
The router is implemented in **`routers/provider_routes.py`** and provides endpoints for **creating, retrieving, updating, and deleting providers**.

### **✅ Provider Router Code (`provider_routes.py`)**
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

---

## **Key Features**
- **Implements RESTful CRUD operations** for provider management.
- **Uses `Depends(get_db)` for dependency injection** to manage database sessions.
- **Handles exceptions** for missing providers with `HTTPException`.
- **Follows the Repository Pattern**, separating API logic from data storage concerns.

---

## **Usage in FastAPI**
The **Provider Router** is registered in `main.py`:
```python
from routers import provider_routes
app.include_router(provider_routes.router)
```

---

## **Conclusion**
The **Provider Router** ensures a **scalable, modular, and maintainable** API structure for managing providers. By following **FastAPI’s dependency injection** and **Repository Pattern**, it supports different storage backends without modifying the API logic.


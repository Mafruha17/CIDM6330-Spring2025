
# Assignment 03: Extend API with a Repository

## **West Texas A&M University**
- **Semester:** Spring 2025  
- **Course:** CIDM6330/01 Software Engineering  
- **Student:** Mafruha Chowdhury  

---

## **Overview**
This assignment extends the **API** built in **Assignment 02** by implementing the **Repository Pattern** to abstract data persistence. The goal is to facilitate **CRUD operations** with multiple storage backends while maintaining clean architecture and separation of concerns.

## **Objectives**
- Implement the **Repository Pattern** to manage data access.
- Support **three persistence strategies**:
  - **SQLModel Repository** (Database-backed storage)
  - **CSV Repository** (File-based storage)
  - **In-Memory Repository** (Ephemeral storage for testing)
- Modify **FastAPI** to dynamically use one of the repositories.
- Ensure a **fully functional API** with persistence across different storage options.

---
Git repo link 
---
[https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment3](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment3)

[EDR for assignment03 ](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment3/docs/edr.PNG)


[EDR CLass Diagram](https://github.com/Mafruha17/CIDM6330-Spring2025/blob/main/Assignment3/docs/Class%20Diagram.png)

---

## **Table of Contents**
1. [Project Overview](#overview)
2. [Repository Pattern & Implementation](#repository-pattern--implementation)
   - [SQLModel Repository](#sqlmodel-repository)
   - [CSV Repository](#csv-repository)
   - [In-Memory Repository](#in-memory-repository)
3. [FastAPI Integration](#fastapi-integration)
4. [Installation & Setup](#installation--setup)
5. [Project Folder Structure](#project-folder-structure)
6. [API Endpoints](#api-endpoints)
7. [CRUD Operations](#crud-operations)
8. [Testing Strategy](#testing-strategy)
9. [Future Improvements](#future-improvements)
10. [Conclusion](#conclusion)
11. [Code Files & Documentation](#code-files--documentation)

---

## **Repository Pattern & Implementation**
This project follows the **Repository Pattern**, where data access is handled by repository classes instead of direct database queries in API routes. Each repository follows the same interface, making it easy to swap implementations.

### **SQLModel Repository**
- Uses **SQLAlchemy + SQLModel** to persist data in a relational database.
- Provides full **CRUD** functionality.
- Uses **session-based transactions** to manage data consistency.

### **CSV Repository**
- Stores and retrieves data in **CSV files** instead of a database.
- Reads/writes data on every API call.
- Suitable for simple persistence without database dependency.

### **In-Memory Repository**
- Stores data in **Python dictionaries** (volatile memory).
- Data is lost when the server restarts.
- Useful for **unit testing** and quick demos.

---

## **FastAPI Integration**
The API dynamically selects the appropriate repository based on an environment variable:

```python
import os
from fastapi import Depends
from repositories.sql_repository import SQLPatientRepository
from repositories.csv_repository import CSVPatientRepository
from repositories.in_memory_repository import InMemoryPatientRepository

def get_patient_repository():
    repo_type = os.getenv("REPO_TYPE", "sql")
    if repo_type == "csv":
        return CSVPatientRepository()
    elif repo_type == "memory":
        return InMemoryPatientRepository()
    else:
        return SQLPatientRepository()

@router.get("/{patient_id}")
def get_patient(patient_id: int, repo=Depends(get_patient_repository)):
    return repo.get(patient_id)
```
Simply change `REPO_TYPE` in the **`.env`** file to switch between different repositories:
```
REPO_TYPE=sql  # Options: sql, csv, memory
```

---

## **Installation & Setup**
Follow these steps to set up and run the API:

### **1. Clone the Repository**
```bash
git clone <repository_url>
cd <repository_name>
```

### **2. Create & Activate a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Database (for SQLModel Repository)**
```bash
rm database/database.db  # Remove old DB (if exists)
python database/create_db.py  # Create a new DB
```

### **5. Configure Environment Variables**
Modify the `.env` file:
```
DATABASE_URL=sqlite:///./database.db
REPO_TYPE=sql  # Options: sql, csv, memory
CSV_PATH=./data
```

### **6. Run FastAPI Server**
```bash
uvicorn main:app --reload
```

---

## **Project Folder Structure**
```
project-root/
│
├── database/
│   ├── crud/
│   │   ├── patient_crud.py
│   │   ├── provider_crud.py
│   │   └── device_crud.py
│   ├── connection.py
│   ├── models.py
│   └── database.db
│
├── repositories/
│   ├── base_repository.py
│   ├── sql_repository.py
│   ├── csv_repository.py
│   ├── in_memory_repository.py
│   ├── patient_repository.py
│   ├── provider_repository.py
│   └── device_repository.py
│
├── routers/
│   ├── patient_routes.py
│   ├── provider_routes.py
│   ├── device_routes.py
│
├── schemas/
│   ├── patient.py
│   ├── provider.py
│   └── device.py
│
├── tests/
│   ├── test_sql_repository.md
│   ├── test_csv_repository.md
│   ├── test_in_memory_repository.md
│   ├── conftest.md
│
├── main.py
├── requirements.txt
├── .gitignore
├── .env
├── README.md
└── docs/
    ├── patient_repository.md
    ├── provider_repository.md
    ├── device_repository.md
```

---

## **API Endpoints**

| **Entity**   | **Method** | **Endpoint**                                      | **Description**                |
| ------------ | ---------- | ------------------------------------------------- | ------------------------------ |
| **Patient**  | **POST**   | `/patients/`                                      | Create a new patient           |
|              | **GET**    | `/patients/{id}`                                  | Retrieve patient details       |
|              | **GET**    | `/patients/`                                      | Retrieve all patients          |
|              | **PUT**    | `/patients/{id}`                                  | Update patient details         |
|              | **DELETE** | `/patients/{id}`                                  | Delete a patient               |
| **Device**   | **POST**   | `/devices/`                                       | Create a new device            |
|              | **GET**    | `/devices/{id}`                                   | Retrieve device details        |
|              | **GET**    | `/devices/`                                       | Retrieve all devices           |
|              | **PUT**    | `/devices/{id}`                                   | Update device details          |
|              | **DELETE** | `/devices/{id}`                                   | Delete a device                |
|              | **POST**   | `/devices/{patient_id}/assign-device/{device_id}` | Assign a device to a patient   |
|              | **DELETE** | `/devices/{patient_id}/remove-device/{device_id}` | Remove a device from a patient |
| **Provider** | **POST**   | `/providers/`                                     | Create a new provider          |
|              | **GET**    | `/providers/{id}`                                 | Retrieve provider details      |
|              | **GET**    | `/providers/`                                     | Retrieve all providers         |
|              | **PUT**    | `/providers/{id}`                                 | Update provider details        |
|              | **DELETE** | `/providers/{id}`                                 | Delete a provider              |
|              | **GET**    | `/providers/{provider_id}/patients`               | Retrieve patients by provider  |

---
## **CRUD Operations**

### **Overview**
This document provides details on the **CRUD (Create, Read, Update, Delete) operations** implemented in Assignment 03. The CRUD functionality ensures that **Patients, Providers, and Devices** can be managed effectively across multiple storage backends (**SQLModel, CSV, and In-Memory**).

CRUD operations are implemented within separate repository classes, allowing a structured and scalable approach to data persistence.

---

### **Table of Contents**
1. [Patient CRUD Operations](#1-patient-crud-operations-databasecrudpatient_crudpy)
2. [Provider CRUD Operations](#2-provider-crud-operations-databasecrudprovider_crudpy)
3. [Device CRUD Operations](#3-device-crud-operations-databasecruddevice_crudpy)
4. [Common Features Across CRUD Methods](#4-common-features-across-crud-methods)
5. [Conclusion](#conclusion)

---

### **1. Patient CRUD Operations (`database/crud/patient_crud.py`)**

#### **✅ CRUD Functions Implemented:**
```python
from sqlmodel import Session
from database.models import Patient
from repositories.patient_repository import PatientRepository
from schemas.patient import PatientSchema

def create_patient(db: Session, patient_data: PatientSchema) -> Patient:
    return PatientRepository(db).create(patient_data)

def get_patient(db: Session, patient_id: int) -> Patient:
    return PatientRepository(db).get(patient_id)

def update_patient(db: Session, patient_id: int, patient_data: PatientSchema) -> Patient:
    return PatientRepository(db).update(patient_id, patient_data)

def delete_patient(db: Session, patient_id: int) -> bool:
    return PatientRepository(db).delete(patient_id)
```
✅ **Ensures patients can be created, retrieved, updated, and deleted** using SQLModel.

---

### **2. Provider CRUD Operations (`database/crud/provider_crud.py`)**

#### **✅ CRUD Functions Implemented:**
```python
from sqlmodel import Session
from database.models import Provider
from repositories.provider_repository import ProviderRepository
from schemas.provider import ProviderSchema

def create_provider(db: Session, provider_data: ProviderSchema) -> Provider:
    return ProviderRepository(db).create(provider_data)

def get_provider(db: Session, provider_id: int) -> Provider:
    return ProviderRepository(db).get(provider_id)

def update_provider(db: Session, provider_id: int, provider_data: ProviderSchema) -> Provider:
    return ProviderRepository(db).update(provider_id, provider_data)

def delete_provider(db: Session, provider_id: int) -> bool:
    return ProviderRepository(db).delete(provider_id)
```
✅ **Handles provider CRUD operations with full repository abstraction.**

---

### **3. Device CRUD Operations (`database/crud/device_crud.py`)**

#### **✅ CRUD Functions Implemented:**
```python
from sqlmodel import Session
from database.models import Device
from repositories.device_repository import DeviceRepository
from schemas.device import DeviceSchema

def create_device(db: Session, device_data: DeviceSchema) -> Device:
    return DeviceRepository(db).create(device_data)

def get_device(db: Session, device_id: int) -> Device:
    return DeviceRepository(db).get(device_id)

def update_device(db: Session, device_id: int, device_data: DeviceSchema) -> Device:
    return DeviceRepository(db).update(device_id, device_data)

def delete_device(db: Session, device_id: int) -> bool:
    return DeviceRepository(db).delete(device_id)
```
✅ **Manages CRUD operations for devices, linking them to patients as necessary.**

---

### **4. Common Features Across CRUD Methods**

#### **🔹 Error Handling & Data Integrity**
- **Exception Handling:** All CRUD methods check if an object exists before performing updates or deletions.
- **Database Transactions:** CRUD operations ensure commit/rollback behavior for data integrity.
- **Foreign Key Constraints:** Prevent accidental deletion of referenced entities (e.g., providers linked to patients).

#### **🔹 Scalability & Repository Pattern**
- **Storage Agnostic:** The same CRUD logic can be used across **SQL, CSV, and In-Memory** repositories.
- **Reusability:** Repository classes abstract away the data persistence logic, making CRUD functions easier to manage.
- **FastAPI Integration:** CRUD functions are designed to be used seamlessly within API routes.

---

### **5. Conclusion**
- **CRUD operations** for Patients, Providers, and Devices are well-defined and follow a structured repository pattern.
- **Multiple repository backends** (SQLModel, CSV, In-Memory) can be easily integrated without modifying the core logic.
- **Error handling and data validation** ensure robust data persistence and integrity.

This documentation serves as a reference for developers implementing and testing CRUD operations in **Assignment 03**. 🚀


---
## **Testing Strategy**

This project includes **unit tests for repositories** and **integration tests for API endpoints** to ensure functionality across multiple storage backends.

### **✅ Running All Tests**
Execute all test cases using `pytest`:
```bash
pytest tests/
```

### **✅ Running Specific Tests**
To run tests for individual repository implementations:
```bash
pytest tests/test_sql_repository.py  # Test SQLModel Repository
pytest tests/test_csv_repository.py  # Test CSV Repository
pytest tests/test_in_memory_repository.py  # Test In-Memory Repository
pytest tests/test_patient.py  # Test Patient API
pytest tests/test_device.py  # Test Device API
pytest tests/test_provider.py  # Test Provider API
```

### **✅ Test Fixtures and Setup**
- **`conftest.py`** provides fixtures for setting up a test database and FastAPI client.
- **SQLite in-memory database** is used for unit tests to ensure isolated execution.
- **Test clients simulate API requests** without requiring a live server.

Example `conftest.py` setup:
```python
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
```

### **✅ API Integration Tests**
- Test patient creation, retrieval, updates, and deletion.
- Test device assignments and provider-patient relationships.

Example API test (`test_patient.py`):
```python
def test_create_patient(client: TestClient):
    response = client.post("/patients/", json={
        "name": "John Doe", "email": "johndoe@example.com", "age": 30, "active": True
    })
    assert response.status_code == 200
```

### **✅ Repository Unit Tests**
- Validate CRUD operations for **SQL, CSV, and In-Memory Repositories**.
- Ensure data persistence and correctness in respective storage.

Example repository test (`test_sql_repository.py`):
```python
def test_create_patient(session):
    repository = SQLPatientRepository(session)
    patient_data = PatientSchema(name="John Doe", email="johndoe@example.com", age=30, active=True)
    created_patient = repository.create(patient_data)
    assert created_patient.id is not None
```
### **✅**Additional FastAPI Testing Strategy **

This project includes comprehensive tests to ensure the FastAPI application functions correctly across different repository implementations and API endpoints.

### **1. Running the FastAPI Server with Uvicorn**
- The FastAPI application is served using **Uvicorn**, an ASGI server.
- To start the server, use the following command:
  ```bash
  uvicorn main:app --reload
  ```
- The `--reload` flag enables automatic reloading on code changes, which is useful for development.

### **2. API Documentation with Swagger UI**
- FastAPI provides automatic API documentation using **Swagger UI** and **ReDoc**.
- After running the FastAPI server, the documentation can be accessed at:
  - **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  - **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- These interfaces allow testing API endpoints directly from the browser.

### **3. FastAPI Unit & Integration Testing**
- Unit tests verify the correctness of repository methods (CRUD operations).
- Integration tests validate API behavior when interacting with repositories.
- Tests ensure FastAPI responses return expected status codes and JSON data.
- Uses **pytest and HTTPX** for API testing.

### **4. Test FastAPI Endpoints Using `pytest` and `httpx`**
- Uses **FastAPI's TestClient** to simulate API calls.
- Ensures endpoints work correctly with different repository implementations.
- Example test case for a FastAPI endpoint using `httpx`:
  ```python
  import httpx
  from fastapi.testclient import TestClient
  from main import app

  client = TestClient(app)

  def test_get_patients():
      response = client.get("/patients/")
      assert response.status_code == 200
  ```

### **5. Seeding Test Data for GET, POST, PUT, DELETE Operations**
- Uses test data seeding to ensure endpoints return expected responses.
- Example of **POST, GET, UPDATE, DELETE** operations for testing:
  ```python
  def test_create_and_get_patient():
      # Create a new patient
      create_response = client.post("/patients/", json={
          "name": "Test Patient",
          "email": "test@example.com",
          "age": 35,
          "active": True
      })
      assert create_response.status_code == 200
      patient_id = create_response.json()["id"]

      # Retrieve the created patient
      get_response = client.get(f"/patients/{patient_id}")
      assert get_response.status_code == 200
      assert get_response.json()["name"] == "Test Patient"

      # Update patient details
      update_response = client.put(f"/patients/{patient_id}", json={
          "id": patient_id,
          "name": "Updated Name",
          "email": "updated@example.com",
          "age": 40,
          "active": False
      })
      assert update_response.status_code == 200

      # Delete patient
      delete_response = client.delete(f"/patients/{patient_id}")
      assert delete_response.status_code == 200
  ```

### **6. Dependency Injection for Testing**
- The `get_db` dependency is overridden to use an **in-memory database** for tests.
- Ensures tests do not affect the production database.

Example of overriding FastAPI dependencies in tests:
```python
@pytest.fixture
def test_app():
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```
---
## **Code Files & Documentation**
For more detailed information on the implementation of each module, refer to the following markdown files:

- [Schema Documentation](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment3/docs/schemas.md)
- [Database & CRUD Operations](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment3/docs/database_CRUD_Operation.md)
- [Repository Documentation ](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment3/docs/repository_pattern_Implementation.md)
- [Router Documentation](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment3/docs/routers.md)
- [Testing doc](https://github.com/Mafruha17/CIDM6330-Spring2025/tree/main/Assignment3/docs/test_documentation.md)

---

## **Future Improvements**
- **Authentication & Authorization** (OAuth2, JWT)
- **Asynchronous Processing** for performance optimization
- **Database Migrations** using **Alembic**
- **Enhanced Logging & Monitoring**
- **FHIR API Integration** (for healthcare standards compliance)

---

## **Conclusion**
This assignment successfully refactors our FastAPI application to use the **Repository Pattern**, supporting **SQL, CSV, and in-memory storage**. It ensures **clean architecture**, improves **testability**, and provides a solid foundation for further enhancements.

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
| **Entity**  | **Method** | **Endpoint**              | **Description**             |
|------------|-----------|---------------------------|-----------------------------|
| **Patient** | **POST**   | `/patients/`             | Create a new patient        |
|             | **GET**    | `/patients/{id}`         | Retrieve patient details    |
|             | **PUT**    | `/patients/{id}`         | Update patient details      |
|             | **DELETE** | `/patients/{id}`         | Delete a patient            |
| **Device**  | **POST**   | `/devices/`              | Create a new device         |
| **Provider**| **POST**   | `/providers/`            | Create a new provider       |

---

## **Code Files & Documentation**
For more detailed information on the implementation of each module, refer to the following markdown files:

- [Schema Documentation](docs/schemas.md)
- [Database & CRUD Operations](docs/database_CRUD_Operation.md)
---
- [Repository Documentation ](docs/repository_pattern_Implementation.md)
    - [Patient Repository](docs/patient_repository.md)
    - [Provider Repository](docs/provider_repository.md)
    - [Device Repository](docs/device_repository.md)
---
- [Router Documentation](docs/routers.md)
  - [Patient Router](docs/patient_router.md)
  - [Provider Router](docs/provider_router.md)
  - [Device Router](docs/device_router.md)
---
- [SQL Repository Tests](tests/test_sql_repository.md)
- [CSV Repository Tests](tests/test_csv_repository.md)
- [In-Memory Repository Tests](tests/test_in_memory_repository.md)
- [Test Configuration](tests/conftest.md)

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

🎯 **Assignment 03 Completed!**
```

Now, you can create those linked `.md` files inside the `docs/` and `tests/` folders, and the main `README.md` will link to them.

Let me know if you need any modifications! 🚀
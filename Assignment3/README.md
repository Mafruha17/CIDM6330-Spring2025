

**West Texas A&M University**  
**Semester:** Spring 2025  
**Course:** CIDM6330/01 Software Engineering  
**Student:** Mafruha Chowdhury

---

# Assignment 03: Extend Your API with a Repository

In this assignment, we build on the **API** created in Assignment 02 by:

1. **Applying the Repository Pattern**: Introducing a dedicated layer that abstracts data access (database, CSV, or in-memory).
2. **Implementing Multiple Repository Options**:
   - **SQLModel/SQL** – Persists data to a database.
   - **CSV** – Reads/writes data in CSV files.
   - **In-Memory** – Stores data in memory only (handy for testing/demos).
3. **Modifying the FastAPI Application** to dynamically switch between these repositories.

> **Important**: This new assignment **extends** your existing code. You’ll keep `models.py`, `schemas/`, CRUD routes, etc. The difference is your routes will now call a repository **interface** rather than talking directly to the DB or CSV.

---

## Table of Contents

1. [Assignment 03 Overview](#assignment-03-overview)
2. [Assignment 02 Recap](#assignment-02-recap)
   - [Entity Selection](#entity-selection)
   - [ERD](#erd)
3. [Repository Pattern in This Project](#repository-pattern-in-this-project)
   - [SQL/SQLModel Repository](#sqlsqlmodel-repository)
   - [CSV Repository](#csv-repository)
   - [In-Memory Repository](#in-memory-repository)
4. [Integration with FastAPI](#integration-with-fastapi)
   - [Choosing Which Repository to Use](#choosing-which-repository-to-use)
5. [Installation & Setup](#installation--setup)
6. [Project Folder Structure](#project-folder-structure)
7. [API Endpoints](#api-endpoints)
8. [Enhancing Database Relationships](#enhancing-database-relationships)
9. [Steps to Optimize and Minimize ERD](#steps-to-optimize-and-minimize-erd)
10. [Future Implementations](#future-implementations-would-be-good-to-have)
11. [CRUD Implementation (Assignment 02 Review)](#crud-implementation-assignment-02-review)
12. [Conclusion](#conclusion)

---

## Assignment 03 Overview

### What’s New?

- **Repositories**: Classes that encapsulate CRUD logic for each data source.
- **Three Storage Options**:  
  1. **SQL** using `SQLModel`/`SQLAlchemy`  
  2. **CSV** for file-based data  
  3. **In-memory** for quick tests and ephemeral data
- **Dependency Injection**: FastAPI routes declare a repository as a dependency (`Depends(...)`), making it easy to **swap** from SQL to CSV or memory.

---

## Assignment 02 Recap

### Entity Selection

The primary healthcare-related entities chosen:
- **Patient**
- **Device**
- **Provider**

### ERD

The **Entity Relationship Diagram (ERD)** below shows relationships among those entities. A **One-to-Many** exists from Patient to Device, and a **Many-to-Many** between Patient and Provider.

![Assignment specific ERD Diagram](./edr/edr.PNG)

---

## Repository Pattern in This Project

### SQL/SQLModel Repository

- Uses SQLAlchemy or SQLModel under the hood.
- Respects your existing `models.py` and `connection.py` to manage the DB session.
- Typical CRUD methods: `create()`, `read()`, `update()`, `delete()`.

### CSV Repository

- Reads/writes entity data in simple CSV files (e.g., `patients.csv`, `devices.csv`, etc.).
- Watch out for concurrency, but for a straightforward assignment or demo, this is fine.

### In-Memory Repository

- Stores entities in Python dictionaries/lists.
- **No** actual file or database.
- Data is lost on server restart but is great for **testing** or ephemeral usage.

---

## Integration with FastAPI

### Choosing Which Repository to Use

One approach is to have an environment variable or config that sets `REPO_TYPE=sql|csv|memory`. Then, in your route dependencies, you can do something like:

```python
import os
from fastapi import Depends

def get_patient_repository():
    repo_type = os.getenv("REPO_TYPE", "sql")
    if repo_type == "csv":
        return CSVPatientRepository()
    elif repo_type == "memory":
        return InMemoryPatientRepository()
    else:
        return SQLPatientRepository()

@router.get("/{patient_id}")
def get_patient(patient_id: int, repo = Depends(get_patient_repository)):
    return repo.read(patient_id)
```

> With this setup, you only need to change `REPO_TYPE` to switch how the data is persisted.

---

## Installation & Setup

| **Step** | **Description** | **Command(s) / Configuration** |
|---------|----------------|--------------------------------|
| 1 | Clone the Repository | ```bash
git clone <repository_url>
cd <repository_name>
``` |
| 2 | Create a Virtual Environment | ```bash
python -m venv venv
``` |
| 3 | Activate Virtual Environment (Windows) | ```bash
.\venv\Scripts\Activate
``` |
| 4 | Activate Virtual Environment (macOS/Linux) | ```bash
source venv/bin/activate
``` |
| 5 | Install Dependencies | ```bash
pip install -r requirements.txt
``` |
| 6 | Setup Database (if using SQL) | ```bash
rm database/database.db
python database/create_db.py
``` |
| 7 | Configure Environment Variables |In your `.env`:
```plaintext
DATABASE_URL=sqlite:///./database.db
REPO_TYPE=sql
CSV_PATH=./data  # For CSV-based repos
```
| 8 | Run the API Server | ```bash
uvicorn main:app --reload
``` |

---

## Project Folder Structure


```plaintext
project-root/
│
├── database/
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── device_crud.py
│   │   ├── patient_crud.py
│   │   └── provider_crud.py
│   ├── connection.py
│   ├── create_db.py
│   ├── models.py
│   └── database.db
│
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py      # Abstract/base class or interface
│   ├── csv_repository.py       # CSV-based repository
│   ├── device_repository.py    # Device-specific repository logic
│   ├── in_memory_repository.py # In-memory repository
│   ├── patient_repository.py   # Patient-specific repository logic
│   ├── provider_repository.py  # Provider-specific repository logic
│   └── sql_repository.py       # SQL-based repository (using SQLAlchemy/SQLModel)
│
├── routers/
│   ├── device_routes.py
│   ├── patient_routes.py
│   └── provider_routes.py
│
├── schemas/
│   ├── device.py
│   ├── patient.py
│   └── provider.py
│
├── tests/
│   ├── conftest.py
│   ├── test_csv_repository.py
│   ├── test_in_memory_repository.py
│   ├── test_sql_repository.py
│   └── __init__.py
│
├── main.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

> You may have additional files/folders (like `docs/`, `utilsclasses/`, etc.) as your project grows.

---

## API Endpoints

> These remain largely the same as Assignment 02. The difference is your code behind the scenes may call repository methods instead of direct DB calls.

| **Entity**  | **Method** | **Endpoint**              | **Description**             |
|------------|-----------|---------------------------|-----------------------------|
| **Patient** | **POST**   | `/patients/`             | Create a new patient        |
|             | **GET**    | `/patients/{patient_id}` | Retrieve patient details    |
|             | **PUT**    | `/patients/{patient_id}` | Update patient details      |
|             | **DELETE** | `/patients/{patient_id}` | Delete a patient            |
| **Device**  | **POST**   | `/devices/`              | Create a new device         |
|             | **GET**    | `/devices/{device_id}`   | Retrieve device details     |
|             | **PUT**    | `/devices/{device_id}`   | Update device details       |
|             | **DELETE** | `/devices/{device_id}`   | Delete a device             |
| **Provider**| **POST**   | `/providers/`            | Create a new provider       |
|             | **GET**    | `/providers/{provider_id}`| Retrieve provider details   |
|             | **PUT**    | `/providers/{provider_id}`| Update provider details     |
|             | **DELETE** | `/providers/{provider_id}`| Delete a provider           |

---

## Enhancing Database Relationships

*(From Assignment 02.)*  
- **Patient ↔ Device**: One-to-Many (a patient can have multiple devices).  
- **Patient ↔ Provider**: Many-to-Many relationship.

### Current Implementation

- Uses `ForeignKey` constraints in `models.py`.  
- You can further refine or optimize with `joinedload()` for fewer queries if using SQL.

---

## Steps to Optimize and Minimize ERD

*(From Assignment 02.)*  
- **Normalization**  
- **Refine Relationships**  
- **Clarify Attribute Types**  

---

## Future Implementations Would Be Good to Have

1. **Authentication & Authorization** (e.g., JWT, OAuth2)  
2. **Asynchronous Processing** for higher concurrency  
3. **Database Migrations** (Alembic)  
4. **Better Logging & Monitoring**  
5. **Integration with FHIR or external healthcare APIs**  
6. **Polymorphic / Inheritance Models** (if your domain demands it)

---

## CRUD Implementation (Assignment 02 Review)

You likely have `crud/` modules for **patients**, **providers**, and **devices**. For example:

- `patient_crud.py` with `create_patient()`, `get_patient()`, `update_patient()`, etc.
- `device_crud.py` for device CRUD.
- `provider_crud.py` for provider CRUD.

For **Assignment 03**, you can either:
1. **Refactor** the logic from these `crud` modules into your new repository classes, **or**  
2. **Keep** the `crud` modules and have your repository classes just *call* those functions.  

**Example** (if you keep `crud` logic):
```python
class SQLPatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, patient_data):
        return create_patient(self.db, patient_data)  # from patient_crud
    ...
```

---

## Conclusion

- **Assignment 03** extends your existing healthcare API by implementing the **Repository Pattern**, allowing easy swaps between **SQL**, **CSV**, or **in-memory** data sources.
- All your previous **ERD**, **CRUD**, and **schemas** remain relevant. The key difference is you now have a **repository layer** to handle data operations, making your app more flexible and testable.

**Congratulations** on taking another step towards scalable, maintainable software design! If you have further customizations (e.g., advanced tests, specialized repos, or concurrency handling), you can build on top of this repository foundation.
# **Test Documentation**

## **Overview**
This document provides an overview of the testing strategy implemented for **Assignment 03**. The test suite ensures that the **Repository Pattern**, **CRUD operations**, and **FastAPI endpoints** function correctly across multiple storage backends (**SQL, CSV, and In-Memory**).

The test suite includes:
- **Unit Tests** for repositories.
- **Integration Tests** for FastAPI endpoints.
- **Test Configuration (`conftest.py`)** for consistent database initialization.

---

## **Table of Contents**
1. [SQL Repository Tests](#sql-repository-tests)
2. [CSV Repository Tests](#csv-repository-tests)
3. [In-Memory Repository Tests](#in-memory-repository-tests)
4. [Test Configuration](#test-configuration)

---

## **1. SQL Repository Tests**
For detailed test cases, refer to the [SQL Repository Tests](tests/test_sql_repository.md).

### **Purpose**
- Ensures that the **SQLModel-based repository** correctly handles **CRUD operations**.
- Tests **database persistence** and **ORM functionality**.
- Uses **SQLite (in-memory) for isolated testing**.

---

## **2. CSV Repository Tests**
For detailed test cases, refer to the [CSV Repository Tests](tests/test_csv_repository.md).

### **Purpose**
- Ensures that **CSV-based storage** correctly supports **CRUD operations**.
- Tests **data persistence and retrieval consistency**.
- Verifies that **CSV files** are properly read and written.

---

## **3. In-Memory Repository Tests**
For detailed test cases, refer to the [In-Memory Repository Tests](tests/test_in_memory_repository.md).

### **Purpose**
- Ensures that the **in-memory repository** correctly implements **CRUD operations**.
- Tests **temporary data persistence** without requiring a database.
- Validates that API endpoints return correct responses when using in-memory storage.

---

## **4. Test Configuration**
For detailed setup and fixtures, refer to the [Test Configuration](tests/conftest.md).

### **Purpose**
- **Defines test fixtures** for **database initialization**.
- Ensures **a fresh test environment** before each test run.
- Provides a **FastAPI TestClient** for **API integration testing**.

Example test configuration (`conftest.py`):
```python
import pytest
from sqlmodel import create_engine, SQLModel, Session
from fastapi.testclient import TestClient
from main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture():
    return TestClient(app)
```

---

## **Conclusion**
This test suite ensures that the **FastAPI application** and **Repository Pattern** function correctly across multiple storage backends (**SQL, CSV, and In-Memory**). By maintaining a structured testing approach, we guarantee **data integrity, API reliability, and flexibility** for future enhancements.

🚀 **Comprehensive testing ensures a stable and maintainable application!**


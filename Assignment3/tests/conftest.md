# **Test Configuration (`conftest.py`)**

## **Overview**
This document outlines the **test configuration setup** in `conftest.py`, which provides reusable test fixtures for **database initialization, session management, and API testing**. The configuration ensures that each test runs in an **isolated environment** to maintain consistency and prevent unwanted dependencies between test cases.

---

## **Test Objectives**
- Provide a **clean database session** for each test.
- Configure **FastAPI’s TestClient** for API integration testing.
- Ensure **SQLite (in-memory) is used** for SQL-based tests to avoid persistent side effects.

---

## **Fixture Implementations**
### **✅ Database Session Fixture**
```python
import pytest
from sqlmodel import create_engine, SQLModel, Session

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
```

#### **Purpose:**
- Initializes an **in-memory SQLite database** before each test.
- Automatically **creates tables** for testing.
- Ensures **a fresh database state** before every test case.

---

### **✅ FastAPI Test Client Fixture**
```python
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(name="client")
def client_fixture():
    return TestClient(app)
```

#### **Purpose:**
- Provides a **TestClient instance** for testing API endpoints.
- Allows API requests to be made **without running a live server**.

---

### **✅ Example Usage in Test Cases**

#### **Testing a GET Request**
```python
def test_get_patient(client):
    response = client.get("/patients/1")
    assert response.status_code == 404  # Ensuring patient does not exist initially
```

#### **Testing a POST Request**
```python
def test_create_patient(client):
    response = client.post("/patients/", json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "age": 30,
        "active": True
    })
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
```

---

## **Conclusion**
The `conftest.py` configuration ensures that **each test runs in an isolated environment**, preventing unwanted test dependencies. By using **in-memory SQLite for database tests** and **FastAPI’s TestClient for API validation**, the test suite guarantees accurate and reliable results while maintaining efficiency.

🚀 **Proper test configuration is crucial for ensuring a stable and maintainable codebase!**


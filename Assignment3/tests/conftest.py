# tests/conftest.py
# tests/conftest.py
import pytest
from sqlmodel import create_engine, SQLModel, Session
from fastapi.testclient import TestClient
import sys
import os

# 🔹 Add the project root to Python's module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.models import Patient
from main import app  # ✅ Ensure 'main.py' is correctly imported

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # ✅ Ensure a fresh start before each test
        session.query(Patient).delete()
        session.commit()
        yield session

@pytest.fixture(name="client")
def client_fixture():
    """
    Provides a test client for making API requests.
    """
    return TestClient(app)

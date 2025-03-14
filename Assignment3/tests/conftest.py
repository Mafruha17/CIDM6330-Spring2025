import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel, Session
import sys
import os

# ✅ Ensure correct module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app  # Ensure 'app' is correctly imported
from database.models import Patient, Device, Provider  # Import models

# ✅ Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="session")
def session_fixture():
    """
    Provides a test database session.
    Uses an in-memory SQLite database for fast, isolated tests.
    """
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.drop_all(engine)  # Ensure clean state
    SQLModel.metadata.create_all(engine)  # Create tables

    with Session(engine) as session:
        yield session  # Provide session to tests

@pytest.fixture(name="client")
def client_fixture():
    """
    Provides a FastAPI test client for API requests.
    """
    assert isinstance(app, FastAPI)  # Ensure app is a FastAPI instance
    return TestClient(app)

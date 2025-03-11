# conftest.py
# tests/conftest.py

import pytest
from sqlmodel import create_engine, SQLModel, Session

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

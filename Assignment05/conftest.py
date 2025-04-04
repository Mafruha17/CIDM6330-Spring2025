import pytest
from ninja.testing import TestClient
from mainapp.api import api

@pytest.fixture(scope="session")
def ninja_client():
    return TestClient(api)

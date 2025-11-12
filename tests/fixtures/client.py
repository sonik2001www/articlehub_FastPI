import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    """Shared FastAPI TestClient."""
    with TestClient(app) as c:
        yield c

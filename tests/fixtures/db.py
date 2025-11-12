import pytest
import mongomock

from fastapi.testclient import TestClient
from app.main import app
from app.db.mongo import get_db
from app.models import USERS_COL, ARTICLES_COL

from .async_db import AsyncDB  # прибери імпорт, якщо async-обгортка не потрібна


@pytest.fixture(scope="session")
def mongo_client():
    """In-memory MongoDB client using mongomock."""
    return mongomock.MongoClient()


@pytest.fixture(scope="session")
def mongo_db(mongo_client):
    """Raw mongomock database instance."""
    return mongo_client["test_db"]


@pytest.fixture(scope="session")
def async_db(mongo_db):
    """Async-style wrapper over mongomock DB."""
    return AsyncDB(mongo_db)


@pytest.fixture(autouse=True)
def override_mongo_db(async_db):
    """
    Override FastAPI get_db dependency with an in-memory MongoDB.

    This fixture is autouse so all tests automatically use the mocked DB.
    """

    async def _get_test_db():
        yield async_db

    app.dependency_overrides[get_db] = _get_test_db
    try:
        yield
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def clear_db(mongo_db):
    """Clear collections before a test that needs a clean DB."""
    mongo_db[USERS_COL].delete_many({})
    mongo_db[ARTICLES_COL].delete_many({})
    return mongo_db

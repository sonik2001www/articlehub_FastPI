import pytest

from app.models import USERS_COL
from app.core.security import hash_password

TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "strong_password_123"
TEST_USER_NAME = "Test User"


@pytest.fixture
def test_user(mongo_db, clear_db):
    """
    Create a default test user in the mocked database.

    Returns a dict with raw (plain) password so tests can use it for login.
    """
    users_col = mongo_db[USERS_COL]

    password_hash = hash_password(TEST_USER_PASSWORD)
    user_doc = {
        "email": TEST_USER_EMAIL,
        "password": password_hash,
        "name": TEST_USER_NAME,
        "is_active": True,
    }

    users_col.insert_one(user_doc)

    return {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
        "name": TEST_USER_NAME,
        "is_active": True,
    }

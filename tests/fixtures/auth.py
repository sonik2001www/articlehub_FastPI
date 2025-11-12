import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def auth_headers(client: TestClient, test_user):
    """
    Log in via real /login endpoint and return Authorization header
    with a Bearer token.
    """
    resp = client.post(
        "/api/auth/login/",
        json={
            "email": test_user["email"],
            "password": test_user["password"],
        },
    )
    assert resp.status_code == 200
    tokens = resp.json()
    access = tokens["access"]
    return {"Authorization": f"Bearer {access}"}

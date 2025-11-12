from fastapi.testclient import TestClient
from .conftest import TEST_USER_EMAIL, TEST_USER_NAME


def test_login_success(client: TestClient, test_user):
    resp = client.post(
        "/api/auth/login/",
        json={"email": test_user["email"], "password": test_user["password"]},
    )

    assert resp.status_code == 200
    data = resp.json()
    assert "access" in data
    assert "refresh" in data


def test_login_wrong_password(client: TestClient, test_user):
    resp = client.post(
        "/api/auth/login/",
        json={"email": test_user["email"], "password": "wrong-password"},
    )

    assert resp.status_code == 401


def test_profile_requires_auth(client: TestClient):
    resp = client.get("/api/auth/profile/")
    assert resp.status_code == 403


def test_profile_ok(client: TestClient, auth_headers):
    resp = client.get("/api/auth/profile/", headers=auth_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == TEST_USER_EMAIL
    assert data["name"] == TEST_USER_NAME
    assert "id" in data

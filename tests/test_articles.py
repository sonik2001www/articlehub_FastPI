from fastapi.testclient import TestClient


def test_article_crud_flow(client: TestClient, auth_headers):
    # --- create ---
    create_resp = client.post(
        "/api/articles/",
        json={
            "title": "My first article",
            "content": "Hello world!",
            "tags": ["test", "fastapi"],
        },
        headers=auth_headers,
    )

    assert create_resp.status_code == 201
    created = create_resp.json()
    article_id = created["id"]
    assert created["title"] == "My first article"
    assert created["content"] == "Hello world!"
    assert set(created["tags"]) == {"test", "fastapi"}

    # --- get ---
    get_resp = client.get(f"/api/articles/{article_id}/", headers=auth_headers)
    assert get_resp.status_code == 200
    got = get_resp.json()
    assert got["id"] == article_id
    assert got["title"] == "My first article"

    # --- update ---
    update_resp = client.put(
        f"/api/articles/{article_id}/",
        json={"title": "Updated title", "content": "New content"},
        headers=auth_headers,
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["id"] == article_id
    assert updated["title"] == "Updated title"
    assert updated["content"] == "New content"

    # --- list ---
    list_resp = client.get("/api/articles/", headers=auth_headers)
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert isinstance(items, list)
    assert any(a["id"] == article_id for a in items)

    # --- delete ---
    delete_resp = client.delete(
        f"/api/articles/{article_id}/",
        headers=auth_headers,
    )
    assert delete_resp.status_code in (200, 204)

    # --- get after delete -> 404 ---
    get_after = client.get(f"/api/articles/{article_id}/", headers=auth_headers)
    assert get_after.status_code == 404

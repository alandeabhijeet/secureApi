from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_success():
    response = client.post("/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    response = client.post("/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401


def test_tasks_without_token():
    response = client.get("/tasks")
    assert response.status_code in (401, 403)


def test_tasks_with_valid_token():
    login_resp = client.post("/login", json={"username": "admin", "password": "admin123"})
    token = login_resp.json()["access_token"]
    response = client.get("/tasks", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "tasks" in response.json()


def test_tasks_with_invalid_token():
    response = client.get("/tasks", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401

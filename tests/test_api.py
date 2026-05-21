from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine

client = TestClient(app)


def setup_module(module):
    # recreate database for tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_and_get_task():
    resp = client.post("/tasks/", json={"title": "Test", "description": "demo"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test"
    task_id = data["id"]

    resp2 = client.get(f"/tasks/{task_id}")
    assert resp2.status_code == 200
    assert resp2.json()["id"] == task_id

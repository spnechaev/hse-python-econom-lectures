from fastapi.testclient import TestClient

from app.main import MemoryTaskRepository, create_app


def test_task_scenario() -> None:
    app = create_app(MemoryTaskRepository())

    with TestClient(app) as client:
        created = client.post("/tasks", json={"title": "Prepare demo", "priority": 5})
        assert created.status_code == 201
        assert created.json() == {
            "id": 1,
            "title": "Prepare demo",
            "priority": 5,
            "done": False,
        }

        completed = client.post("/tasks/1/done")
        assert completed.status_code == 200
        assert completed.json()["done"] is True

        response = client.get("/tasks")
        assert response.status_code == 200
        assert len(response.json()) == 1


def test_validation_and_not_found() -> None:
    with TestClient(create_app(MemoryTaskRepository())) as client:
        assert client.post("/tasks", json={"title": "", "priority": 9}).status_code == 422
        assert client.post("/tasks/999/done").status_code == 404

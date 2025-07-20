from fastapi.testclient import TestClient
import pytest

from .main import CreateTask, app

client = TestClient(app)

INITIAL_TASKS = [
    CreateTask(name="Test task 1", isCompleted=False),
    CreateTask(name="Test task 2", isCompleted=True),
    CreateTask(name="Test task 3", isCompleted=False),
]


@pytest.fixture
def app_init():
    app.set_tasks(INITIAL_TASKS)


def test_read_tasks(app_init):
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == [
        {"name": "Test task 1", "isCompleted": False, "id": 0},
        {"name": "Test task 2", "isCompleted": True, "id": 1},
        {"name": "Test task 3", "isCompleted": False, "id": 2},
    ]


def test_create_task(app_init):
    # Make sure we start with 3 tasks
    response = client.get("/tasks")
    assert response.status_code == 200
    all_tasks = response.json()
    assert len(all_tasks) == 3

    response = client.post("/tasks", json={"name": "Test task 4", "isCompleted": False})
    assert response.status_code == 201
    task = response.json()
    assert task == {"name": "Test task 4", "isCompleted": False, "id": 3}

    # We should now have 4 tasks
    response = client.get("/tasks")
    assert response.status_code == 200
    all_tasks = response.json()
    assert len(all_tasks) == 4

from fastapi.testclient import TestClient
import pytest

from backend.main import CreateTask, app

client = TestClient(app)

INITIAL_TASKS = [
    CreateTask(name="Test task 1", isCompleted=False),
    CreateTask(name="Test task 2", isCompleted=True),
    CreateTask(name="Test task 3", isCompleted=False),
]


def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    # Ensure we have an HTML page that mentions the docs
    assert response.headers["Content-Type"].find("text/html") >= 0
    page = response.content.decode("utf-8")
    assert page.find("docs") >= 0


@pytest.fixture
def app_init():
    """
    A fixture to ensure that the backend is initialized with a known set of tasks. This ensures reproducible testing.
    """
    app.set_tasks(INITIAL_TASKS)


def test_read_tasks(app_init):
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == [
        {"name": "Test task 1", "isCompleted": False, "id": "0"},
        {"name": "Test task 2", "isCompleted": True, "id": "1"},
        {"name": "Test task 3", "isCompleted": False, "id": "2"},
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
    assert task == {"name": "Test task 4", "isCompleted": False, "id": "3"}

    # We should now have 4 tasks
    response = client.get("/tasks")
    assert response.status_code == 200
    all_tasks = response.json()
    assert len(all_tasks) == 4


def test_get_task(app_init):
    response = client.get("/tasks/0")
    assert response.status_code == 200
    task = response.json()
    assert task == {"id": "0", "name": "Test task 1", "isCompleted": False}

    response = client.get("/tasks/-1")
    assert response.status_code == 404


def test_delete_task(app_init):
    # Existing task
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    response = client.get("/tasks")
    assert len(response.json()) == 2

    # Nonexistent task
    response = client.delete("/tasks/1")
    assert response.status_code == 404


def test_update_task(app_init):
    # Ensure we can update one property at a time
    route = "/tasks/0"
    original_task = client.get(route).json()
    # 1. Update nothing
    response = client.put(route, json={})
    assert response.status_code == 201
    assert response.json() == original_task
    assert response.json() == client.get(route).json()

    # 2. Update name
    new_name = "Updated name"
    response = client.put(route, json={"name": new_name})
    new_task = response.json()
    assert response.status_code == 201
    assert new_task == {
        "name": new_name,
        "isCompleted": original_task["isCompleted"],
        "id": original_task["id"],
    }
    assert new_task == client.get(route).json()

    # 3. Update completed
    response = client.put(route, json={"isCompleted": not original_task["isCompleted"]})
    new_task = response.json()
    assert response.status_code == 201
    assert new_task == {
        "name": new_name,
        "isCompleted": not original_task["isCompleted"],
        "id": original_task["id"],
    }
    assert new_task == client.get(route).json()

    # 4. Update both
    new_name = "Another new name"
    response = client.put(
        route, json={"isCompleted": original_task["isCompleted"], "name": new_name}
    )
    new_task = response.json()
    assert response.status_code == 201
    assert new_task == {
        "name": new_name,
        "isCompleted": original_task["isCompleted"],
        "id": original_task["id"],
    }
    assert new_task == client.get(route).json()

    # Invalid task
    response = client.put("/tasks/-1", json={})
    assert response.status_code == 404

import traceback
from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient

from backend.main import CreateTask, app
from backend.task import Task
from backend.task_list import InMemoryTaskList, DbTaskList

client = TestClient(app)

INITIAL_TASKS = [
    CreateTask(name="Test task 1", isCompleted=False),
    CreateTask(name="Test task 2", isCompleted=True),
    CreateTask(name="Test task 3", isCompleted=False),
]


# Fixture to switch between MongoDB and in memory storage
@pytest.fixture(autouse=True, scope="module", params=[DbTaskList, InMemoryTaskList])
def set_local_scope(request):
    # Note: We must use TestClient in with here to trigger the lifespan events:
    #   https://stackoverflow.com/a/75727846/3297440
    with TestClient(app) as client:
        try:
            orig_tasks = app.state.task_list
            app.state.task_list = request.param()
            yield
        finally:
            app.state.task_list = orig_tasks


def _task_to_route(task: Task):
    return f"/tasks/{task.id}"


@pytest.fixture
def app_init():
    """A fixture to ensure that the backend is initialized with a known set of tasks. This ensures reproducible testing.

    Returns list of tasks the database was initialized with
    """
    app.state.task_list.set_tasks(INITIAL_TASKS)
    # Sort tasks by name for predictable behavior
    task_dict = app.state.task_list.tasks()
    task_list = list(task_dict.values())
    task_list.sort(key=lambda t: t.name)
    yield task_list


def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    # Ensure we have an HTML page that mentions the docs
    assert response.headers["Content-Type"].find("text/html") >= 0
    page = response.content.decode("utf-8")
    assert page.find("docs") >= 0


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "healthy"}


def test_read_tasks(app_init):
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == [
        {"name": "Test task 1", "isCompleted": False, "id": ANY},
        {"name": "Test task 2", "isCompleted": True, "id": ANY},
        {"name": "Test task 3", "isCompleted": False, "id": ANY},
    ]
    # Ensure IDs are unique
    ids = {t["id"] for t in data}
    assert len(ids) == len(data), f"Task IDs are not unique: {ids}"


def test_create_task(app_init):
    # Make sure we start with 3 tasks
    response = client.get("/tasks")
    assert response.status_code == 200
    all_tasks = response.json()
    assert len(all_tasks) == 3

    response = client.post("/tasks", json={"name": "Test task 4", "isCompleted": False})
    assert response.status_code == 201
    task = response.json()
    assert task == {"name": "Test task 4", "isCompleted": False, "id": ANY}

    # We should now have 4 tasks
    response = client.get("/tasks")
    assert response.status_code == 200
    all_tasks = response.json()
    assert len(all_tasks) == 4


def test_get_task(app_init):
    task_list = app_init
    # Sort tasks by name for predictable behavior
    orig_task = task_list[0]
    response = client.get(_task_to_route(orig_task))
    assert response.status_code == 200
    task = response.json()
    assert task == {
        "id": orig_task.id,
        "name": orig_task.name,
        "isCompleted": orig_task.isCompleted,
    }

    response = client.get("/tasks/-1")
    assert response.status_code == 404


def test_delete_task(app_init):
    # Existing task
    task_list = app_init
    task = task_list[0]
    delete_route = _task_to_route(task)
    response = client.delete(delete_route)
    assert response.status_code == 204
    response = client.get("/tasks")
    assert len(response.json()) == 2

    # Nonexistent task
    response = client.delete(delete_route)
    assert response.status_code == 404


def test_update_task(app_init):
    # Ensure we can update one property at a time
    task_list = app_init
    route = _task_to_route(task_list[0])
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

import pytest
from backend.dbinterface import MongoDBInterface
from backend.task import CreateTask, Task, UpdateTask

DB_NAME = "test_todo_app"


@pytest.fixture
def get_db():
    db = MongoDBInterface(DB_NAME)
    assert db.num_tasks() == 0
    yield db
    db._task_collection.drop()
    assert db.num_tasks() == 0


def test_create_task(get_db):
    db = get_db
    assert db.num_tasks() == 0
    task_info = CreateTask(name="Task 1", isCompleted=False)
    new_task = db.create_task(task_info)
    assert task_info.name == new_task.name
    assert task_info.isCompleted == new_task.isCompleted
    assert new_task.id is not None
    assert new_task.id != ""


def test_delete_task(get_db):
    db = get_db
    task_info = CreateTask(name="Task 1", isCompleted=False)
    new_task = db.create_task(task_info)
    assert db.num_tasks() == 1
    # Delete existing task
    num_deleted = db.delete_task(new_task.id)
    assert num_deleted == 1
    assert db.num_tasks() == 0
    # Delete non-existent task
    num_deleted = db.delete_task(new_task.id)
    assert num_deleted == 0
    assert db.num_tasks() == 0


def test_get_task(get_db):
    db = get_db
    task_info = CreateTask(name="Task 1", isCompleted=False)
    new_task = db.create_task(task_info)
    assert db.num_tasks() == 1
    new_task_lookup = db.get_task(new_task.id)
    assert new_task_lookup == new_task


def test_update_task(get_db):
    db = get_db
    task_info = CreateTask(name="Task 1", isCompleted=False)
    new_task = db.create_task(task_info)
    assert db.num_tasks() == 1
    # 1. Updating with no params should do nothing
    updated_task = db.update_task(new_task.id, UpdateTask())
    assert updated_task == new_task
    # 2. Update name only TODO
    # 3. Update isCompleted only TODO
    # 4. Update both TODO
    # 5. Update non-existent TODO

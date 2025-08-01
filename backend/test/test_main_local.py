"""Backend tests for the FastAPI backend using in-memory task list for storage"""

import pytest

from backend.task_list import InMemoryTaskList
from backend.test.main_template import *


# Force local storage for these tests
@pytest.fixture(autouse=True, scope="module")
def set_local_scope():
    with TestClient(app) as client:
        try:
            orig_tasks = app.state.task_list
            app.state.task_list = InMemoryTaskList()
        finally:
            app.state.task_list = orig_tasks

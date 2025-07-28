from fastapi import FastAPI, status
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import validate_call
from typing import List, Literal
import os

from backend.dbinterface import MongoDBInterface
from backend.task import (
    CreateTask,
    Task,
    UpdateTask,
    TaskId,
)
from backend.task_list import TaskList, InMemoryTaskList, DbTaskList


class TodoFastAPI(FastAPI):
    _task_list: TaskList

    @validate_call
    def __init__(
        self,
        data_source: Literal["local"] | Literal["db"],
        initial_tasks: List[CreateTask],
    ):
        super().__init__()
        self._data_source = data_source
        if self._data_source == "local":
            self._task_list = InMemoryTaskList()
            self._task_list.set_tasks(initial_tasks)
        elif self._data_source == "db":
            if len(initial_tasks) > 0:
                raise RuntimeError("Initial tasks not supported in database mode")
            self._task_list = DbTaskList()

    def task_list(self):
        return self._task_list

    def set_tasks(self, tasks: List[CreateTask]):
        self._task_list.set_tasks(tasks)


app = TodoFastAPI(
    data_source="local",
    initial_tasks=[
        CreateTask(name="Task 1", isCompleted=False),
        CreateTask(name="Task 2", isCompleted=False),
        CreateTask(name="Task 3", isCompleted=False),
    ],
)

## TODO make this actually secure
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return FileResponse(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "index.html")
    )


@app.get("/tasks")
async def tasks() -> List[Task]:
    return list(app.task_list().tasks().values())


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(input_task: CreateTask, response: Response) -> Task:
    new_task = app.task_list().create_task(
        name=input_task.name, isCompleted=input_task.isCompleted
    )
    response.headers["Location"] = f"/tasks/{new_task.id}"
    return new_task


@app.get("/tasks/{id}")
async def get_task(id: TaskId, response: Response):
    task = app.task_list().get_task(id)
    if task is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    return task


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: TaskId, response: Response):
    if app.task_list().delete_task(id):
        return
    # Didn't find it
    response.status_code = 404


@app.put("/tasks/{id}", status_code=status.HTTP_201_CREATED)
async def update_task(id: TaskId, body: UpdateTask, response: Response) -> Task | None:
    updated = app.task_list().update_task(id, body)
    if updated is None:
        response.status_code = 404
        return
    return updated

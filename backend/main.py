from contextlib import asynccontextmanager
import os
from typing import Annotated, List, Literal

from fastapi import Depends, FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import validate_call

from backend import settings
from backend.task import CreateTask, Task, TaskId, UpdateTask
from backend.task_list import DbTaskList, InMemoryTaskList, TaskList


@asynccontextmanager
async def lifespan(app: FastAPI):
    match settings.BACKEND_MODE:
        case "db":
            task_list = DbTaskList()
        case "local":
            task_list = InMemoryTaskList()
    print(f"Setting task list")
    app.state.task_list = task_list
    print(f"State: {app.state.task_list}")
    yield
    task_list.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return FileResponse(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "index.html")
    )


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/tasks")
async def tasks() -> List[Task]:
    tasks = list(app.state.task_list.tasks().values())
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(input_task: CreateTask, response: Response) -> Task:
    new_task = app.state.task_list.create_task(
        name=input_task.name, isCompleted=input_task.isCompleted
    )
    response.headers["Location"] = f"/tasks/{new_task.id}"
    return new_task


@app.get("/tasks/{id}")
async def get_task(id: TaskId, response: Response):
    task = app.state.task_list.get_task(id)
    if task is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    return task


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: TaskId, response: Response):
    if app.state.task_list.delete_task(id):
        return
    # Didn't find it
    response.status_code = 404


@app.put("/tasks/{id}", status_code=status.HTTP_201_CREATED)
async def update_task(id: TaskId, body: UpdateTask, response: Response) -> Task | None:
    updated = app.state.task_list.update_task(id, body)
    if updated is None:
        response.status_code = 404
        return
    return updated

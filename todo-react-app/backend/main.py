from fastapi import FastAPI, status
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import validate_call
from typing import List, Literal


from backend.task import TaskList, CreateTask, Task, UpdateTask, InMemoryTaskList


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
            self._task_list = InMemoryTaskList(tasks={}, _next_id=0)
            self._task_list.set_tasks(initial_tasks)

    def task_list(self):
        if self._data_source == "local":
            return self._task_list
        else:
            raise RuntimeError("db mode not implemented")

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
    return FileResponse("index.html")


@app.get("/tasks")
async def tasks() -> List[Task]:
    return list(app.task_list().tasks.values())


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(input_task: CreateTask, response: Response) -> Task:
    new_task = app.task_list().create_task(
        name=input_task.name, isCompleted=input_task.isCompleted
    )
    response.headers["Location"] = f"/tasks/{new_task.id}"
    return new_task


@app.get("/tasks/{id}")
async def get_task(id: str, response: Response):
    task = app.task_list().tasks.get(id)
    if task is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    return task


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: str, response: Response):
    if app.task_list().delete_task(id):
        return
    # Didn't find it
    response.status_code = 404


@app.put("/tasks/{id}", status_code=status.HTTP_201_CREATED)
async def update_task(id: str, body: UpdateTask, response: Response) -> Task | None:
    if id not in app.task_list().tasks:
        response.status_code = 404
        return
    if body.isCompleted is not None:
        app.task_list().tasks[id].isCompleted = body.isCompleted
    if body.name is not None:
        app.task_list().tasks[id].name = body.name
    return app.task_list().tasks[id]

from fastapi import FastAPI, status
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validate_call
from typing import List, Literal
from typing import Dict


class CreateTask(BaseModel):
    name: str
    isCompleted: bool


class Task(BaseModel):
    name: str
    isCompleted: bool
    id: int


class TaskList(BaseModel):
    tasks: Dict[int, Task]
    next_id: int

    def create_task(self, isCompleted: bool, name: str) -> Task:
        task = Task(isCompleted=isCompleted, name=name, id=self.get_next_id())
        self.tasks[task.id] = task
        return task

    def delete_task(self, id: int) -> bool:
        if id in self.tasks:
            del self.tasks[id]
            return True
        return False

    def get_next_id(self):
        res = self.next_id
        self.next_id += 1
        return res


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
            self.set_tasks(initial_tasks)

    def task_list(self):
        if self._data_source == "local":
            return self._task_list
        else:
            raise RuntimeError("db mode not implemented")

    def set_tasks(self, tasks: List[CreateTask]):
        task_list = map(
            lambda id, task: Task(isCompleted=task.isCompleted, name=task.name, id=id),
            range(len(tasks)),
            tasks,
        )
        next_id = len(tasks)
        task_dict = dict(zip(range(len(tasks)), task_list))
        self._task_list = TaskList(tasks=task_dict, next_id=next_id)


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
    return {"message": "Hello, world"}


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


class IdParam(BaseModel):
    id: int


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int, response: Response):
    if app.task_list().delete_task(id):
        return
    # Didn't find it
    response.status_code = 404


@app.put("/tasks/{id}", status_code=status.HTTP_201_CREATED)
async def update_task(id: int, body: CreateTask, response: Response) -> Task | None:
    if id not in app.task_list().tasks:
        response.status_code = 404
        return

    app.task_list().tasks[id].isCompleted = body.isCompleted
    app.task_list().tasks[id].name = body.name
    return app.task_list().tasks[id]

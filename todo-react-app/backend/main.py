from fastapi import FastAPI, status
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from typing import Dict

app = FastAPI()
## TODO make this actually secure
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateTask(BaseModel):
    name: str
    isCompleted: bool


class Task(BaseModel):
    name: str
    isCompleted: bool
    id: int


TASK_ID: int = 4


class TaskList(BaseModel):
    tasks: Dict[int, Task] = {
        1: Task(name="Task 1", isCompleted=False, id=1),
        2: Task(name="Task 2", isCompleted=False, id=2),
        3: Task(name="Task 3", isCompleted=True, id=3),
    }
    _next_id = 4

    def next_id(self):
        res = self._next_id
        self._next_id += 1
        return res


task_list = TaskList()


@app.get("/")
async def root():
    return {"message": "Hello, world"}


@app.get("/tasks")
async def tasks() -> List[Task]:
    return list(task_list.tasks.values())


# TODO there's a better way to return this info, right?
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(input_task: CreateTask) -> Task:
    new_task = Task(
        name=input_task.name, isCompleted=input_task.isCompleted, id=task_list.next_id()
    )
    task_list.tasks[new_task.id] = new_task
    return new_task


class IdParam(BaseModel):
    id: int


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int, response: Response):
    if id in task_list.tasks:
        # TODO what's the right status / return stuff?
        del task_list.tasks[id]
        return

    # Didn't find it
    response.status_code = 404


@app.put("/tasks/{id}", status_code=status.HTTP_201_CREATED)
async def update_task(id: int, body: CreateTask, response: Response) -> Task | None:
    if id not in task_list.tasks:
        response.status_code = 404
        return

    task_list.tasks[id].isCompleted = body.isCompleted
    task_list.tasks[id].name = body.name
    # TODO what to return?
    return task_list.tasks[id]

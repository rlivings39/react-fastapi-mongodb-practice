from pydantic import BaseModel
from typing import Optional, Dict

type TaskId = str

type TaskDict = Dict[TaskId, Task]


class CreateTask(BaseModel):
    name: str
    isCompleted: bool


class Task(CreateTask):
    id: TaskId


class UpdateTask(BaseModel):
    name: Optional[str] = None
    isCompleted: Optional[bool] = None

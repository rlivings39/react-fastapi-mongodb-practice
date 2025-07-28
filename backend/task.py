from typing import Dict, Optional

from pydantic import BaseModel

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

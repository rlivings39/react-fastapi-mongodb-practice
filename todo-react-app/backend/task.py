from pydantic import BaseModel
from typing import Optional
from typing import Dict


class CreateTask(BaseModel):
    name: str
    isCompleted: bool


class UpdateTask(BaseModel):
    name: Optional[str] = None
    isCompleted: Optional[bool] = None


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

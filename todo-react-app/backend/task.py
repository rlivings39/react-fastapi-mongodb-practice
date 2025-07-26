from pydantic import BaseModel
from typing import List, Optional
from typing import Dict
from abc import ABC, abstractmethod


class CreateTask(BaseModel):
    name: str
    isCompleted: bool


class UpdateTask(BaseModel):
    name: Optional[str] = None
    isCompleted: Optional[bool] = None


class Task(BaseModel):
    name: str
    isCompleted: bool
    id: str


class TaskList(ABC):
    tasks: Dict[str, Task]

    @abstractmethod
    def create_task(self, isCompleted: bool, name: str) -> Task:
        pass

    @abstractmethod
    def delete_task(self, id: str) -> bool:
        pass

    @abstractmethod
    def get_next_id(self):
        pass

    @abstractmethod
    def set_tasks(self, tasks: List[CreateTask]):
        pass


class DbTaskList(BaseModel, TaskList):
    tasks: Dict[str, Task]
    _next_id: int

    def create_task(self, isCompleted: bool, name: str) -> Task:
        task = Task(isCompleted=isCompleted, name=name, id=self.get_next_id())

        return task

    def delete_task(self, id: int) -> bool:
        if id in self.tasks:
            del self.tasks[id]
            return True
        return False

    def get_next_id(self):
        res = self._next_id
        self._next_id += 1
        return str(res)

    def set_tasks(self, tasks: List[CreateTask]):
        raise NotImplementedError("set_tasks not implemented for DB storage")


class InMemoryTaskList(BaseModel, TaskList):
    tasks: Dict[str, Task]
    _next_id: int

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
        res = self._next_id
        self._next_id += 1
        return str(res)

    def set_tasks(self, tasks: List[CreateTask]):
        task_list = map(
            lambda id, task: Task(
                isCompleted=task.isCompleted, name=task.name, id=str(id)
            ),
            range(len(tasks)),
            tasks,
        )
        self._next_id = len(tasks)
        self.tasks = {t.id: t for t in task_list}

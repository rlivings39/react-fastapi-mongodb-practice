from abc import ABC, abstractmethod
from typing import List

from backend.dbinterface import MongoDBInterface
from backend.task import CreateTask, Task, TaskDict, TaskId, UpdateTask


class TaskList(ABC):

    @abstractmethod
    def tasks(self) -> TaskDict:
        pass

    @abstractmethod
    def create_task(self, isCompleted: bool, name: str) -> Task:
        pass

    @abstractmethod
    def delete_task(self, id: TaskId) -> bool:
        pass

    @abstractmethod
    def get_task(self, id: TaskId) -> Task | None:
        pass

    @abstractmethod
    def update_task(self, id: TaskId, update_params: UpdateTask) -> Task | None:
        pass

    @abstractmethod
    def set_tasks(self, tasks: List[CreateTask]):
        pass


class DbTaskList(TaskList):
    def __init__(self, *v, **kw):
        super().__init__(*v, **kw)
        self._db: MongoDBInterface = MongoDBInterface()

    def tasks(self) -> TaskDict:
        return self._db.get_all_tasks()

    def get_task(self, id: TaskId) -> Task | None:
        return self._db.get_task(id)

    def update_task(self, id: TaskId, update_params: UpdateTask) -> Task | None:
        return self._db.update_task(id, update_params)

    def create_task(self, isCompleted: bool, name: str) -> Task:
        task = self._db.create_task(CreateTask(isCompleted=isCompleted, name=name))
        return task

    def delete_task(self, id: TaskId) -> bool:
        del_count = self._db.delete_task(id)
        return del_count == 1

    def set_tasks(self, tasks: List[CreateTask]):
        self._db.set_tasks(tasks)


class InMemoryTaskList(TaskList):
    def __init__(self, *v, **kw):
        super().__init__(*v, **kw)
        self._next_id: int = 0
        self._tasks: TaskDict = {}

    def tasks(self) -> TaskDict:
        return self._tasks

    def get_task(self, id: TaskId) -> Task | None:
        return self._tasks.get(id)

    def update_task(self, id: TaskId, update_params: UpdateTask) -> Task | None:
        if id not in self._tasks:
            return None
        if update_params.isCompleted is not None:
            self._tasks[id].isCompleted = update_params.isCompleted
        if update_params.name is not None:
            self._tasks[id].name = update_params.name
        return self._tasks[id]

    def create_task(self, isCompleted: bool, name: str) -> Task:
        task = Task(isCompleted=isCompleted, name=name, id=self.get_next_id())
        self._tasks[task.id] = task
        return task

    def delete_task(self, id: int) -> bool:
        if id in self._tasks:
            del self._tasks[id]
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
        self._tasks = {t.id: t for t in task_list}

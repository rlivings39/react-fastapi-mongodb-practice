from typing import Dict, List
from pymongo import MongoClient
from bson.objectid import ObjectId
from backend.task import Task, CreateTask, TaskId, UpdateTask, TaskDict
from backend import settings


def _document_to_task(doc: Dict):
    task = Task(
        id=str(doc["_id"]),
        name=doc["name"],
        isCompleted=doc["isCompleted"],
    )
    return task


def _task_to_document(task: Task | CreateTask | UpdateTask) -> Dict:
    task_dict = dict(task)
    task_dict = {key: value for key, value in task_dict.items() if value is not None}
    return task_dict


def _id_to_query(id: TaskId) -> Dict[str, ObjectId] | None:
    """Converts an ID string to a valid MongoDB query

    Returns query dictionary or `None` if the provided `id` is not a valid :class:`ObjectId`
    """
    try:
        oid = ObjectId(id)
    except:
        return None
    return {"_id": oid}


class MongoDBInterface:
    def __init__(self, db_name: str = "todo_app"):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = settings.MONGODB_URI

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        self._client = MongoClient(CONNECTION_STRING)

        # Create the database for our example (we will use the same database throughout the tutorial
        self._db = self._client[db_name]
        self._task_collection = self._db["tasks"]

    def get_task(self, id: TaskId) -> Task | None:
        query = _id_to_query(id)
        if query is None:
            return None
        result = self._task_collection.find_one(query)
        if result is None:
            return None
        task = _document_to_task(result)
        return task

    def create_task(self, task: CreateTask) -> Task:
        result = self._task_collection.insert_one(_task_to_document(task))
        return Task(
            id=str(result.inserted_id), name=task.name, isCompleted=task.isCompleted
        )

    def delete_task(self, id: TaskId) -> int:
        query = _id_to_query(id)
        if query is None:
            return 0
        result = self._task_collection.delete_one(query)
        return result.deleted_count

    def update_task(self, id: TaskId, update_params: UpdateTask) -> Task | None:
        query = _id_to_query(id)
        if query is None:
            return None
        update = {"$set": _task_to_document(update_params)}
        response = self._task_collection.update_one(query, update, upsert=False)
        if response.matched_count == 0:
            return None
        return self.get_task(id)

    def num_tasks(self) -> int:
        return self._task_collection.count_documents({})

    def get_all_tasks(self) -> TaskDict:
        task_list = self._task_collection.find()
        task_dict = {t["_id"]: _document_to_task(t) for t in task_list}
        return task_dict

    def print_tasks(self):
        for task in self._task_collection.find():
            print(task)

    def set_tasks(self, tasks: List[CreateTask]):
        self._task_collection.drop()
        for task in tasks:
            self.create_task(task)


if __name__ == "__main__":
    db = MongoDBInterface()
    db.print_tasks()

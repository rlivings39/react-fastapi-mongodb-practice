from pymongo import MongoClient
from bson.objectid import ObjectId

from backend.task import Task, CreateTask


def _task_to_document(task: Task | CreateTask):
    return dict(task)


class MongoDBInterface:
    def __init__(self, db_name: str = "todo_app"):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = "mongodb://localhost:27017/"

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        self._client = MongoClient(CONNECTION_STRING)

        # Create the database for our example (we will use the same database throughout the tutorial
        self._db = self._client[db_name]
        self._task_collection = self._db["tasks"]

    def create_task(self, task: CreateTask) -> Task:
        result = self._task_collection.insert_one(_task_to_document(task))
        return Task(
            id=str(result.inserted_id), name=task.name, isCompleted=task.isCompleted
        )

    def num_tasks(self):
        return self._task_collection.count_documents({})

    def print_tasks(self):
        for task in self._task_collection.find():
            print(task)


if __name__ == "__main__":
    db = MongoDBInterface()
    db.print_tasks()

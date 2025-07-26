from pymongo import MongoClient
from bson.objectid import ObjectId


def get_todo_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client["todo_app"]


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

    # Get the database
    dbname = get_todo_database()
    task_collection = dbname["tasks"]
    # doc = task_collection.insert_one({"name": "Task 1", "isCompleted": False})
    for task in task_collection.find():
        print(task)

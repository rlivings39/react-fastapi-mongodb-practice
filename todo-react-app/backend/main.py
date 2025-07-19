from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    name: str
    isCompleted: bool
    id: int

task_list: List[Task] = [
   Task(name="Task 1", isCompleted=False, id=1),
   Task(name="Task 2", isCompleted=False, id=1),
                         ]

@app.get('/')
async def root():
  return {"message": "Hello, world"}

@app.get('/tasks')
async def tasks():
  return task_list



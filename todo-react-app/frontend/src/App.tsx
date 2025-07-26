import { useState } from "react";
import "./App.css";
import TaskInputBox from "./components/TaskInputBox";
import TodoItem from "./components/TodoItem";

function reportError(message: string, e: unknown) {
  console.error(`${message}\n${e}`);
  if (e instanceof Error) {
    console.error(e.stack);
  }
}

export type TaskId = string;

export class Task {
  constructor(
    public name: string,
    public isCompleted: boolean,
    public id: TaskId
  ) {}
}

export type TaskMap = Record<TaskId, Task>;
function App(props: { initialTasks: TaskMap }) {
  const [tasks, setTasks] = useState<TaskMap>(props.initialTasks);
  const taskElementList = Object.entries(tasks).map(([id, task]) => (
    <TodoItem
      key={id}
      task={task}
      deleteTask={deleteTask}
      markTaskCompleted={setTaskComplete}
      editTask={editTask}
    />
  ));
  async function deleteTask(id: TaskId) {
    try {
      const resp = await fetch(`http://localhost:8000/tasks/${id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
      });
      if (resp.ok) {
        const newTasks = { ...tasks };
        delete newTasks[id];
        setTasks(newTasks);
      }
    } catch (e) {
      reportError("Failed to delete", e);
    }
  }

  async function updateTask(
    id: TaskId,
    edits: { isCompleted?: boolean; name?: string }
  ) {
    try {
      const task = tasks[id];
      if (!task) {
        return;
      }
      const isCompleted = edits.isCompleted ?? task.isCompleted;
      const name = edits.name ?? task.name;
      const resp = await fetch(`http://localhost:8000/tasks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          isCompleted,
        }),
      });
      if (resp.ok) {
        const newTask = (await resp.json()) as Task;
        const newTasks = { ...tasks, [id]: newTask };
        setTasks(newTasks);
      }
    } catch (e) {
      reportError(`Failed to update task`, e);
    }
  }

  function setTaskComplete(id: TaskId) {
    updateTask(id, { isCompleted: true });
  }

  function editTask(id: TaskId, name: string) {
    updateTask(id, { name });
  }

  async function addTask(name: string) {
    try {
      const resp = await fetch("http://localhost:8000/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, isCompleted: false }),
      });
      if (resp.ok) {
        const newTask = (await resp.json()) as Task;
        const newTasks = { ...tasks, [newTask.id]: newTask };
        setTasks(newTasks);
      }
    } catch (e) {
      reportError("Failed to create task", e);
    }
  }

  return (
    <>
      <h1>To Do List</h1>
      <TaskInputBox addTask={addTask} />
      {taskElementList}
    </>
  );
}

export default App;

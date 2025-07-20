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
export class Task {
  constructor(
    public name: string,
    public isCompleted: boolean,
    public id: number
  ) {}
}
function App(props: { initialTasks: Task[] }) {
  const [taskId, setTaskId] = useState(0);
  // TODO make this a map
  const [tasks, setTasks] = useState<Task[]>(props.initialTasks);
  const taskElementList = tasks.map((task) => (
    <TodoItem
      key={task.id}
      task={task}
      deleteTask={deleteTask}
      markTaskCompleted={setTaskComplete}
      editTask={editTask}
    />
  ));
  async function deleteTask(id: number) {
    try {
      const resp = await fetch(`http://localhost:8000/tasks/${id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
      });
      if (resp.ok) {
        // TODO do we need to maintain this state like this or just ask server?
        const filteredTasks = tasks.filter((task) => task.id !== id);
        setTasks(filteredTasks);
      }
    } catch (e) {
      reportError("Failed to delete", e);
    }
  }

  async function updateTask(
    id: number,
    edits: { isCompleted?: boolean; name?: string }
  ) {
    try {
      const task = tasks.find((t) => t.id === id);
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
        // TODO can I make this simpler?
        const newTask = (await resp.json()) as Task;
        const fixedTasks = tasks.map((task) => {
          if (task.id === id) {
            return newTask;
          } else {
            return { ...task };
          }
        });
        setTasks(fixedTasks);
      }
    } catch (e) {
      reportError(`Failed to update task`, e);
    }
  }

  function setTaskComplete(id: number) {
    updateTask(id, { isCompleted: true });
  }

  function editTask(id: number, name: string) {
    updateTask(id, { name });
  }

  async function addTask(name: string) {
    try {
      const resp = await fetch("http://localhost:8000/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, isCompleted: false }),
      });

      // TODO is ok the right check?
      if (resp.ok) {
        const newTask = (await resp.json()) as Task;
        const newTasks = [...tasks, newTask];
        setTaskId(taskId + 1);
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

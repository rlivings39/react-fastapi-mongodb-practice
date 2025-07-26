import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App, { Task, type TaskMap } from "./App.tsx";
let initialTaskArray: Task[] = [];
const initialTasks: TaskMap = {};
try {
  const resp = await fetch("http://localhost:8000/tasks");
  if (resp.ok) {
    // TODO how to ensure type consistency
    initialTaskArray = (await resp.json()) as Task[];
  }
} catch (e) {
  console.error(`Failed to fetch tasks: ${e}`);
}
initialTaskArray.forEach((t) => (initialTasks[t.id] = t));

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App initialTasks={initialTasks} />
  </StrictMode>
);

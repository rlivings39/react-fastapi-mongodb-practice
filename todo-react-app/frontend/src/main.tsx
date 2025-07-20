import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App, { Task } from "./App.tsx";
let initialTasks: Task[] = [];
try {
  const resp = await fetch("http://localhost:8000/tasks");
  if (resp.ok) {
    // TODO how to ensure type consistency
    initialTasks = (await resp.json()) as Task[];
    console.log(initialTasks);
  }
} catch (e) {
  console.error(`Failed to fetch tasks: ${e}`);
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App initialTasks={initialTasks} />
  </StrictMode>
);

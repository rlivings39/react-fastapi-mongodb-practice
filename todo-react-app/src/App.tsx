import { useState } from "react";
// import reactLogo from "./assets/react.svg";
// import viteLogo from "/vite.svg";
import "./App.css";
import TaskInputBox from "./TaskInputBox";
import TodoList from "./TodoList";

export class Task {
  constructor(
    public name: string,
    public isCompleted: boolean,
    public id: number
  ) {}
}
const TASKS: Task[] = [
  { isCompleted: false, name: "First task", id: 1 },
  { isCompleted: false, name: "Second task", id: 2 },
  { isCompleted: true, name: "Completed task", id: 3 },
];

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <h1>To Do List</h1>
      <TaskInputBox />
      <TodoList tasks={TASKS} />
    </>
  );
}

export default App;

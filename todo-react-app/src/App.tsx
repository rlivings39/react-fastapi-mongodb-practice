import { useState } from "react";
// import reactLogo from "./assets/react.svg";
// import viteLogo from "/vite.svg";
import "./App.css";
import TaskInputBox from "./TaskInputBox";
import TodoItem from "./TodoItem";

export class Task {
  constructor(
    public name: string,
    public isCompleted: boolean,
    public id: number
  ) {}
}
function App() {
  const [taskId, setTaskId] = useState(0);
  const [tasks, setTasks] = useState<Task[]>([]);
  const taskElementList = tasks.map((task) => (
    <TodoItem
      key={task.id}
      task={task}
      deleteTask={deleteTask}
      markTaskCompleted={setTaskComplete}
      editTask={editTask}
    />
  ));
  function deleteTask(id: number) {
    const filteredTasks = tasks.filter((task) => task.id !== id);
    setTasks(filteredTasks);
  }

  function setTaskComplete(id: number) {
    const fixedTasks = tasks.map((task) => {
      if (task.id === id) {
        return { ...task, isCompleted: true };
      } else {
        return { ...task };
      }
    });
    setTasks(fixedTasks);
  }

  function addTask(name: string) {
    const newTasks = [...tasks, { isCompleted: false, name, id: taskId }];
    setTaskId(taskId + 1);
    setTasks(newTasks);
  }

  function editTask(id: number, name: string) {
    const editedTasks = tasks.map((task) => {
      if (task.id === id) {
        return { ...task, name };
      } else {
        return { ...task };
      }
    });
    setTasks(editedTasks);
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

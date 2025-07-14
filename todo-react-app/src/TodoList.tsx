import { useState } from "react";
import { Task } from "./App";

function TodoList(props: { tasks: Task[] }) {
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

  function renderTask(task: Task) {
    return (
      <div className="todo-item" key={task.id}>
        <span className={task.isCompleted ? "completed-task" : ""}>
          {" "}
          {task.name}{" "}
        </span>
        <div className="task-button-holder">
          <button
            className="plain-button"
            title="Mark task completed"
            onClick={() => setTaskComplete(task.id)}
          >
            <span className="material-symbols-outlined icon">check</span>
          </button>
          <button className="plain-button" title="Edit task">
            <span className="material-symbols-outlined icon">edit</span>
          </button>
          <button
            className="plain-button"
            title="Delete task"
            onClick={() => deleteTask(task.id)}
          >
            <span className="material-symbols-outlined icon">delete</span>
          </button>
        </div>
      </div>
    );
  }
  const [tasks, setTasks] = useState(props.tasks);
  const taskElements = tasks.map(renderTask);
  return <>{taskElements}</>;
}

export default TodoList;

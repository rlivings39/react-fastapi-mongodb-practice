import { Task } from "./App";

type TaskFunction = (id: number) => void;

function TodoItem(props: {
  task: Task;
  deleteTask: TaskFunction;
  markTaskCompleted: TaskFunction;
}) {
  return (
    <div className="todo-item">
      <span className={props.task.isCompleted ? "completed-task" : ""}>
        {" "}
        {props.task.name}{" "}
      </span>
      <div className="task-button-holder">
        <button
          className="plain-button"
          title="Mark task completed"
          onClick={() => props.markTaskCompleted(props.task.id)}
        >
          <span className="material-symbols-outlined icon">check</span>
        </button>
        <button className="plain-button" title="Edit task">
          <span className="material-symbols-outlined icon">edit</span>
        </button>
        <button
          className="plain-button"
          title="Delete task"
          onClick={() => props.deleteTask(props.task.id)}
        >
          <span className="material-symbols-outlined icon">delete</span>
        </button>
      </div>
    </div>
  );
}

export default TodoItem;

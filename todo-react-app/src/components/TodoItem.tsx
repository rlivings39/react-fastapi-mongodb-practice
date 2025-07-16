import { useRef, useState, useEffect } from "react";
import { Task } from "../App";

type TaskFunction = (id: number) => void;

function TodoItem(props: {
  task: Task;
  deleteTask: TaskFunction;
  markTaskCompleted: TaskFunction;
  editTask: (id: number, name: string) => void;
}) {
  const [isEditing, setIsEditing] = useState(false);
  const [newTaskName, setNewTaskName] = useState(props.task.name);
  const editInputRef = useRef<HTMLInputElement>(null);
  useEffect(() => {
    if (isEditing) {
      editInputRef.current?.focus();
    }
  }, [editInputRef, isEditing]);
  const displayTaskTemplate = (
    <>
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
        <button
          className="plain-button"
          title="Edit task"
          onClick={() => {
            setIsEditing(true);
          }}
        >
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
    </>
  );

  const editTaskTemplate = (
    // Performing the submission tasks here in onSubmit avoids the
    // "Form is not connected" warning seen when doing this in the
    // button's onClick
    <form
      onSubmit={(e) => {
        e.preventDefault();
        setIsEditing(false);
        props.editTask(props.task.id, newTaskName);
      }}
    >
      <input
        type="text"
        value={newTaskName}
        onChange={(e) => setNewTaskName(e.target.value)}
        ref={editInputRef}
      />
      <div className="task-button-holder">
        <button className="plain-button" title="Submit task" type="submit">
          <span className="material-symbols-outlined icon">check</span>
        </button>
        <button
          className="plain-button"
          title="Cancel editing"
          onClick={() => {
            setIsEditing(false);
          }}
          type="button"
        >
          <span className="material-symbols-outlined icon">close</span>
        </button>
      </div>
    </form>
  );

  return (
    <div className="todo-item">
      {isEditing ? editTaskTemplate : displayTaskTemplate}
    </div>
  );
}

export default TodoItem;

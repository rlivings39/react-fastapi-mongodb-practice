import { useState } from "react";

function TaskInputBox(props: { addTask: (name: string) => void }) {
  const [name, setName] = useState("");

  return (
    <>
      {" "}
      <form onSubmit={(e) => e.preventDefault()} className="todo-input-form">
        <input
          className="rounded-input"
          type="text"
          placeholder="Add your task"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button
          className="plain-button task-button-holder"
          onClick={() => {
            if (name === "") {
              return;
            }
            props.addTask(name);
            setName("");
          }}
        >
          <span className="material-symbols-outlined icon add-icon">add</span>
        </button>
      </form>
    </>
  );
}

export default TaskInputBox;

import { useState } from "react";

function TaskInputBox(props: { addTask: (name: string) => void }) {
  const [name, setName] = useState("");

  return (
    <>
      {" "}
      <div id="todo-input">
        <input
          type="text"
          placeholder="Add your task"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button
          className="plain-button"
          onClick={() => {
            props.addTask(name);
            setName("");
          }}
        >
          <span className="material-symbols-outlined icon add-icon">add</span>
        </button>
      </div>
    </>
  );
}

export default TaskInputBox;

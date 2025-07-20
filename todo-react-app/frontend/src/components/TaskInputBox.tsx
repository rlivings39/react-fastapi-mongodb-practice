import { useState } from "react";

function TaskInputBox(props: { addTask: (name: string) => void }) {
  const [name, setName] = useState("");
  // const inputRef = useRef<HTMLInputElement>(null);
  // const [firstTime, setFirstTime] = useState(true);
  // useEffect(() => {
  //   if (firstTime) {
  //     inputRef.current?.focus();
  //     setFirstTime(false);
  //   }
  // }, [inputRef, firstTime]);

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
            const newName = name.trim();
            if (newName === "") {
              return;
            }
            props.addTask(newName);
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

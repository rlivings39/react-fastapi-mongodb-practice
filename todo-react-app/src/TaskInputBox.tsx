function TaskInputBox() {
  return (
    <>
      {" "}
      <div id="todo-input">
        <input type="text" placeholder="Add your task" />
        <button className="plain-button">
          <span className="material-symbols-outlined icon add-icon">add</span>
        </button>
      </div>
    </>
  );
}

export default TaskInputBox;

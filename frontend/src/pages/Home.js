import React, { useState } from "react";
import { Link } from "react-router-dom";

function Home() {
  const [model, setModel] = useState("");
  const [task, setTask] = useState("");

  const modelOptions = ["GPT-3.5", "Mistral", "Llama"];
  const taskOptions = ["Optimization", "Security-Vulnerability-Finding", "Code-Refactoring"];

  // Handle model selection
  const onModelOptionChangeHandler = (event) => {
    setModel(event.target.value);
    console.log("Selected Model:", event.target.value);
  };

  // Handle task selection
  const onTaskChangeHandler = (event) => {
    setTask(event.target.value);
    console.log("Selected Task:", event.target.value);
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", textAlign: "center", marginTop: "50px" }}>
      <h1>Welcome to the Model Inference App</h1>
      <p>Select a model and task to proceed with your inference.</p>

      {/* Model Selection Dropdown */}
      <div style={{ margin: "20px 0" }}>
        <label htmlFor="model-select" style={{ fontWeight: "bold", marginRight: "10px" }}>
          Choose Model:
        </label>
        <select
          id="model-select"
          onChange={onModelOptionChangeHandler}
          style={{
            padding: "8px",
            border: "1px solid #ddd",
            borderRadius: "4px",
            fontSize: "14px",
          }}
        >
          <option value="">-- Please choose a model --</option>
          {modelOptions.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>

      {/* Task Selection Dropdown */}
      <div style={{ margin: "20px 0" }}>
        <label htmlFor="task-select" style={{ fontWeight: "bold", marginRight: "10px" }}>
          Choose Task:
        </label>
        <select
          id="task-select"
          onChange={onTaskChangeHandler}
          style={{
            padding: "8px",
            border: "1px solid #ddd",
            borderRadius: "4px",
            fontSize: "14px",
          }}
        >
          <option value="">-- Please choose a task --</option>
          {taskOptions.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>

      {/* Navigation Button */}
      <Link
        to={`/model-operation?model=${encodeURIComponent(model)}&task=${encodeURIComponent(task)}`}
      >
        <button
          style={{
            padding: "10px 20px",
            backgroundColor: model && task ? "#007BFF" : "#ccc",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            fontSize: "16px",
            cursor: model && task ? "pointer" : "not-allowed",
          }}
          disabled={!model || !task}
        >
          Go to Model Inference
        </button>
      </Link>
    </div>
  );
}

export default Home;

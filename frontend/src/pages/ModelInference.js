import React, { useState } from "react";
import { useLocation, useSearchParams } from "react-router-dom";

const ModelInference = () => {
  const [inputText, setInputText] = useState("");
  const [response, setResponse] = useState("");

  // Extract query parameters
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const model = searchParams.get("model");
  const operation = searchParams.get("task");

  // Handle file upload and parse content
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      setInputText(event.target.result);
    };
    reader.readAsText(file);
    
  };

  // Handle submit to send input to the backend
  const handleSubmit = async () => {
    try {
      const input = inputText;
      if (!model || !operation) {
        setResponse("Model or operation is missing from query parameters.");
        return;
      }

      setResponse("Processing...");

      // Choose the endpoint based on the model and operation
      let endpoint = "";
      if (model === "Mistral" && operation === "Optimization") {
        endpoint = "/generate/optimize-mistral";
      } 
      else if (model === "Mistral" && operation === "Security-Vulnerability-Finding") {
        endpoint = "/generate/security-mistral";
      } 
      else if (model === "Mistral" && operation === "Code-Refactoring") {
        endpoint = "/generate/refractor-mistral";
      }
      else if (model === "GPT-3.5" && operation === "Optimization") {
        endpoint = "/generate/optimize-gpt";
      }
      else if (model === "GPT-3.5" && operation === "Security-Vulnerability-Finding") {
        endpoint = "/generate/security-gpt";
      }
      else if (model === "GPT-3.5" && operation === "Code-Refactoring") {
        endpoint = "/generate/security-gpt";
      }
      else if (model === "Llama" && operation === "Optimization") {
        endpoint = "/generate/security-llama";
      }
      else if (model === "Llama" && operation === "Security-Vulnerability-Finding") {
        endpoint = "/generate/security-llama";
      }
      else if (model === "Llama" && operation === "Code-Refactoring") {
        endpoint = "/generate/security-llama";
      }
      else {
        setResponse("Unsupported model or operation combination.");
        return;
      }

      const ngrokUrl = "https://3273-34-56-87-104.ngrok-free.app"; // Replace with your ngrok URL
      const localBaseUrl = "http://localhost:8000";
     
      const baseUrl = endpoint.includes("gpt") ? localBaseUrl: ngrokUrl;
      console.log("Constructed endpoint:", `${ngrokUrl}${endpoint}`);
      // Send input to the backend{
      const res = await fetch(`${baseUrl}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: input }),
      });


      const result = await res.json();
      console.log(result);
      setResponse(result.response || "No response received.");
    } catch (error) {
      console.error("Error during inference:", error);
      setResponse("Error occurred. Check console for details.");
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", margin: "20px" }}>
      <h1>Model Inference</h1>
      <p>
        <strong>Selected Model:</strong> {model || "None"} <br />
        <strong>Selected Operation:</strong> {operation || "None"}
      </p>

      {/* Text Input */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ fontWeight: "bold", display: "block", marginBottom: "10px" }}>
          Paste your code:
        </label>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          rows="10"
          style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "4px" }}
        ></textarea>
      </div>

      {/* File Upload */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ fontWeight: "bold", display: "block", marginBottom: "10px" }}>
          Or upload a file:
        </label>
        <input type="file" onChange={handleFileUpload} />
      </div>

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        style={{
          padding: "10px 20px",
          backgroundColor: "#007BFF",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        Submit
      </button>

      {/* Model Response */}
      {response && (
        <div style={{ marginTop: "20px" }}>
          <h2>Model Response:</h2>
          <pre
            style={{
              backgroundColor: "#f8f9fa",
              padding: "10px",
              border: "1px solid #ddd",
              borderRadius: "4px",
              overflowX: "auto",
            }}
          >
            {response}
          </pre>
        </div>
      )}
    </div>
  );
};

export default ModelInference;

import React, { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [qaList, setQaList] = useState([]); // List of questions and answers

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
    } else {
      alert("Please upload a valid PDF file.");
      e.target.value = ""; // Reset file input
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      if (response.ok) {
        alert(result.message);
      } else {
        alert(result.error || "Failed to upload the file.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const handleAskQuestion = async () => {
    if (!file) {
      alert("Please upload a PDF first!");
      return;
    }

    if (!question.trim()) {
      alert("Please enter a question.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/ask/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const result = await response.json();
      const answer = result.answer || result.error || "Error processing the question.";

      // Add the question and answer to the list
      setQaList([...qaList, { question, answer }]);
      setQuestion(""); // Clear input field
    } catch (error) {
      console.error("Error asking question:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-left">AI PLANET</div>
        <div className="upload-btn-container">
          <input
            type="file"
            id="file-input"
            accept="application/pdf"
            style={{ display: "none" }}
            onChange={handleFileChange}
          />
          <button
            className="upload-btn"
            onClick={() => document.getElementById("file-input").click()}
          >
            Choose File
          </button>
          <button className="upload-btn" onClick={handleUpload}>
            Upload
          </button>
        </div>
      </header>

      <div className="upload-section">
        {file && <p>File selected: {file.name}</p>}
      </div>

      <div className="qa-list">
        {qaList.map((qa, index) => (
          <div key={index} className="qa-item">
            <p><strong>Question:</strong> {qa.question}</p>
            <p><strong>Answer:</strong> {qa.answer}</p>
            <hr />
          </div>
        ))}
      </div>

      <div className="qa-section">
        <input
          type="text"
          placeholder="Ask your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={handleAskQuestion}>Ask</button>
      </div>
    </div>
  );
}

export default App;



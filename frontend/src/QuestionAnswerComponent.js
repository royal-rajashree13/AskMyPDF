import React, { useState } from 'react';

const QuestionAnswerComponent = () => {
  const [pdfData, setPdfData] = useState(null); // Store uploaded PDF data
  const [question, setQuestion] = useState(""); // Store user's question
  const [answer, setAnswer] = useState(""); // Store answer from backend

  // Handle file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/upload/", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      setPdfData(data); // Save PDF data
    } else {
      alert("Failed to upload PDF");
    }
  };

  // Handle question submission
  const handleQuestionSubmit = async () => {
    if (!question || !pdfData) return; // Ensure question and PDF are available

    try {
      const response = await fetch("http://127.0.0.1:8000/ask/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          pdf_id: pdfData.pdf_id, // Send PDF ID with the question
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setAnswer(data.answer); // Display the answer
      } else {
        alert("Failed to get an answer");
      }
    } catch (error) {
      alert("An error occurred while asking the question");
    }
  };

  return (
    <div className="question-answer-container">
      {/* Upload PDF button */}
      <input type="file" accept=".pdf" onChange={handleFileUpload} id="pdf-upload" style={{ display: "none" }} />
      <label htmlFor="pdf-upload" className="upload-btn">
        Upload PDF
      </label>

      {/* Show uploaded PDF info */}
      {pdfData && (
        <div className="pdf-info">
          <p>Uploaded PDF: {pdfData.file_name}</p>
        </div>
      )}

      {/* Text area to ask questions */}
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question about the PDF..."
        rows="4"
      ></textarea>

      {/* Submit question button */}
      <button onClick={handleQuestionSubmit} className="submit-btn">
        Get Answer
      </button>

      {/* Display answer */}
      {answer && (
        <div className="answer">
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default QuestionAnswerComponent;

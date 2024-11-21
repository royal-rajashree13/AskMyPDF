AskMyPDF
AskMyPDF is a web application that allows users to upload PDF documents and interact with them using natural language queries. Built using FastAPI for the backend and React.js for the frontend, this application leverages advanced NLP models for answering questions related to the uploaded PDF content.
---------------------
Table of Contents
---------------------
Project Overview
Technologies Used
Installation and Setup
Usage
API Endpoints
File Structure
Contributing
-----------------
Project Overview
-----------------
AskMyPDF is designed to simplify the process of querying PDF documents. Users can upload a PDF file and ask natural language questions based on its content. The backend uses FastAPI for efficient API handling, and the NLP processing is handled by the Transformer models. The frontend is built with React.js, providing a seamless user experience.
==================
Technologies Used
===================
Backend: FastAPI
NLP Processing: Transformer (for question answering and text processing)
Frontend: React.js
Database: SQLite or PostgreSQL (for storing document metadata, if necessary)
File Storage: Local filesystem or cloud storage (AWS S3 for storing uploaded PDFs)
========================
Installation and Setup
========================
Backend Setup (FastAPI)

Clone the repository:

===> git clone https://github.com/royal-rajashree13/AskmyPDF.git
===> cd AskmyPDF

Create and activate a virtual environment:

===>python3 -m venv venv
===>source venv/bin/activate  # For Linux/MacOS
===>.\venv\Scripts\activate  # For Windows

Install required dependencies:

===> pip install -r backend/requirements.txt

Run the FastAPI server:
===>uvicorn backend.main:app --reload

The backend should now be running at http://127.0.0.1:8000.
=========================================================================
Frontend Setup (React.js)
Navigate to the frontend directory:
cd frontend

Install frontend dependencies:
npm install

Start the React development server:
npm start

The frontend will be available at http://localhost:3000.
=================================================================================
Usage
Upload a PDF File:
Once the app is running, visit the homepage. You will see an option to upload a PDF file. Choose a valid PDF file and click on the "Upload" button.

Ask a Question:
After uploading the file, enter a question in the provided input box and press the "Ask" button. The system will process the PDF and attempt to answer your question based on its contents.

View Results:
The response will be displayed below the input box, showing the answer retrieved from the uploaded PDF.
============================================================================================
API Endpoints
=>POST /upload/
-Description: Upload a PDF document.
-Request Body:
file: The PDF file to be uploaded.
-Response:
Success message or error message.
=>POST /ask/
-Description: Ask a question about the uploaded PDF document.
-Request Body:
-question: The question you want to ask regarding the PDF content.
-Response:
-answer: The response based on the document content, or an error message if something goes wrong.
=======================================================================================
File Structure

AskMyPDF/
│
├── backend/                      # FastAPI Backend
│   ├── main.py                   # Main FastAPI app
│   ├── models.py                 # Data models (for metadata, etc.)
│   ├── utils.py                  # Helper functions (for NLP processing)
│   └── requirements.txt          # Python dependencies
│
├── frontend/                     # React.js Frontend
│   ├── src/
│   │   ├── components/           # React components (e.g., file upload, Q&A)
│   │   ├── App.js                # Main React App file
│   │   └── index.js              # Entry point
│   └── package.json              # Node.js dependencies
│
├── README.md                     # This README file
└── .gitignore                    # Git ignore file

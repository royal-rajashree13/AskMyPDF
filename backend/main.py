from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import PyPDF2
import os
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss  # For fast nearest neighbor search
from transformers import BartForConditionalGeneration, BartTokenizer
from datetime import datetime
from sqlalchemy.orm import Session
from db import init_db, PDFMetadata, get_db  # Import from your db.py

# Initialize the FastAPI app
app = FastAPI()

# Allow CORS for communication between frontend and backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the SentenceTransformer model for semantic search
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize BART for summarization
summarization_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
summarization_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

uploaded_pdf_text = ""  # Global variable to store uploaded PDF text
text_chunks = []        # To store chunked text for semantic search
index = None            # FAISS index for efficient similarity search
chunk_size = 500        # Size of each text chunk

class Question(BaseModel):
    question: str

# Initialize the database (this should be run once)
init_db()

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text from PDF: {str(e)}")

def split_text_into_chunks(text: str, chunk_size=500):
    """Split the extracted text into smaller chunks of specified size."""
    words = text.split()  # Split by words
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(" ".join(current_chunk)) > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def get_embeddings(text_list):
    """Generate embeddings for the provided text list."""
    return model.encode(text_list, convert_to_numpy=True)

def summarize_text(text: str) -> str:
    """Summarize the provided text using the BART model."""
    inputs = summarization_tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = summarization_model.generate(inputs, max_length=200, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = summarization_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload and process the PDF file."""
    global uploaded_pdf_text, text_chunks, index

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a valid PDF file.")

    file_path = f"uploaded_pdfs/{file.filename}"
    try:
        os.makedirs("uploaded_pdfs", exist_ok=True)  # Create directory if not exists
        with open(file_path, "wb") as temp_file:
            temp_file.write(file.file.read())
        
        # Extract text from the uploaded PDF
        uploaded_pdf_text = extract_text_from_pdf(file_path)

        # Split the text into chunks
        text_chunks = split_text_into_chunks(uploaded_pdf_text, chunk_size=chunk_size)

        # Generate embeddings and build FAISS index
        embeddings = get_embeddings(text_chunks)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)  # L2 distance-based index
        index.add(embeddings)

        # Save PDF metadata to the database
        pdf_metadata = PDFMetadata(
            filename=file.filename,
            upload_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            text_content=uploaded_pdf_text
        )
        db.add(pdf_metadata)
        db.commit()

        # Print success message on the server side
        print(f"PDF '{file.filename}' uploaded and processed successfully!")

        return {"message": "PDF uploaded and processed successfully", "filename": file.filename}
    except Exception as e:
        return {"error": f"Error processing the file: {str(e)}"}

@app.post("/ask/")
async def ask_question(question: Question, db: Session = Depends(get_db)):
    """Answer a question based on the uploaded PDF."""
    global index, text_chunks

    if index is None:  # Check if the FAISS index is built
        return {"error": "No PDF uploaded. Please upload a PDF first."}

    try:
        # Encode the question and find nearest neighbors
        question_embedding = model.encode([question.question], convert_to_numpy=True)
        distances, indices = index.search(question_embedding, k=3)  # Fetch top 3 results

        # Retrieve the most relevant chunks and clean them
        relevant_chunks = [text_chunks[i].strip() for i in indices[0]]  # Strip leading/trailing spaces

        # Combine relevant chunks into one answer string
        answer = "\n\n".join(relevant_chunks)

        # Return the clean answer
        return {"answer": answer}

    except Exception as e:
        return {"error": f"Error processing the question: {str(e)}"}

@app.post("/summarize/")
async def summarize_pdf():
    """Summarize the uploaded PDF document."""
    if not uploaded_pdf_text:
        raise HTTPException(status_code=400, detail="No PDF uploaded. Please upload a PDF first.")

    try:
        # Generate a summary of the entire PDF text
        summary = summarize_text(uploaded_pdf_text)
        return {"summary": summary}
    except Exception as e:
        return {"error": f"Error summarizing the document: {str(e)}"}

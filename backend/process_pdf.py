import PyPDF2
from transformers import pipeline

# Function to extract text from PDF
def extract_pdf_text(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Initialize a variable to hold the text extracted from each page
            full_text = ""
            
            # Iterate through all the pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                full_text += page.extract_text()  # Extract text from each page
                
        return full_text

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# Function to save extracted text to a file
def save_pdf_text(pdf_text):
    try:
        # Open the file with UTF-8 encoding to handle all characters
        with open('output.txt', 'w', encoding='utf-8') as file:
            file.write(pdf_text)
    except Exception as e:
        print(f"Error saving text: {e}")

# Function to save question and answer to a file
def save_qa_to_file(question, answer):
    try:
        with open('qa_output.txt', 'w', encoding='utf-8') as file:
            file.write(f"Question: {question}\n")
            file.write(f"Answer: {answer}\n")
    except Exception as e:
        print(f"Error saving question and answer: {e}")

# Function to answer questions using Hugging Face's pre-trained QA model
def answer_question(question, context_text):
    try:
        # Load the pre-trained question-answering pipeline from Hugging Face
        qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
        
        # Prepare the input for the model
        answer = qa_pipeline(question=question, context=context_text)
        
        return answer['answer']
    
    except Exception as e:
        print(f"Error in answering question: {e}")
        return None

# Main function to process the PDF and handle Q&A
def process_pdf_and_answer_question(pdf_path, question):
    # Extract text from PDF
    extracted_text = extract_pdf_text(pdf_path)
    
    # If extraction was successful, save the text to a file and process the question
    if extracted_text:
        save_pdf_text(extracted_text)
        print("PDF text saved successfully!")
        
        # Answer the question based on the extracted text
        answer = answer_question(question, extracted_text)
        
        if answer:
            print(f"Answer to your question: {answer}")
            save_qa_to_file(question, answer)  # Save the Q&A to file
            print("Question and answer saved successfully!")
        else:
            print("Could not find an answer.")
    else:
        print("Failed to extract text from the PDF.")

# Example usage:
pdf_path = r"C:\Users\rajas\OneDrive\soloProjects\PDF-QA-App\backend\sample.pdf"
question = "What is the main topic of the document?"  # Replace with your question
process_pdf_and_answer_question(pdf_path, question)

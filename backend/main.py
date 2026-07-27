from fastapi import FastAPI, Form, File, UploadFile
from pydantic import BaseModel
from services.llm_service import ask_llm
from fastapi.middleware.cors import CORSMiddleware
import fitz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QuestionRequest(BaseModel): #Main model for user requests, which contains a question and the mode of the chatbot
    question: str
    mode: str

@app.get("/")
def home():
    return{"message": "Academic Assistant API Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}


#User sends a request through the /ask endpoint

@app.post("/ask")                        
async def ask_question(
    question: str = Form(...),
    mode: str = Form(...),
    file: UploadFile = File(...)
    ):
    pdf_bytes = await file.read()

    pdf_document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    extracted_text = ""

    for page in pdf_document:
        extracted_text += page.get_text()

    pdf_document.close()
    
    ai_response = ask_llm(
        question,
        mode,
        extracted_text[:12000]
    )

    return {
        "response": ai_response
    }
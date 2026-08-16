from fastapi import FastAPI, Depends, Form, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag.query_data import get_context
from rag.create_database import create_database
from ai.models.gemini import GeminiAI 
from auth.throttling import apply_rate_limit
#from auth.dependencies import get_user_identifier
import os
import shutil
from dotenv import find_dotenv, load_dotenv

#App initalization
app = FastAPI()

#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["http://localhost:5173"],
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)

#Main model for user requests, which contains a question and the mode of the chatbot

#class QuestionRequest(BaseModel): 
#    question : str = Form(...)
 #   mode : str = Form(...)
 #   file : UploadFile = File(...)

#Since using Form, UploadFile for Pdf logic this Pydantic model will not work

#Main model for AI responses 

class AIResponse(BaseModel): 
    response: str

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("enviornment variable not set")

ai_platform = GeminiAI(API_KEY)

DATA_PATH = "data/docs"


#User sends a request through the /ask endpoint
@app.post("/ask", response_model= AIResponse)                        
async def ask_question(question: str = Form(...), mode: str = Form(...), file: UploadFile = File(...)):

    # Make sure directory exists
    os.makedirs(DATA_PATH, exist_ok=True)

    # Build complete path to uploaded file
    file_path = os.path.join(DATA_PATH, file.filename)

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Rate limit
    apply_rate_limit("global-unauthenticated-user")
    
    # Build Chroma DB from uploaded PDF
    create_database(file_path)

    # Retrieve relevant chunks
    context = get_context(question)

    print("CONTEXT SENT TO GEMINI:")
    print(context)

    # Ask Gemini
    ai_response = ai_platform.chat(
        question,
        mode,
        context
    )

    return AIResponse(response=ai_response)

#Health check
    
@app.get("/")
async def root():
    return {"message" : "API is running"}
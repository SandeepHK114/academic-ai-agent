from fastapi import FastAPI
from pydantic import BaseModel
from services.llm_service import ask_llm
from fastapi.middleware.cors import CORSMiddleware

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
def ask_question(request: QuestionRequest): #FASTAPI then coverts this JSON into a readable QuestionRequest object using Pydantic

    ai_response = ask_llm(request.question, request.mode) #naviagte to ask_llm within llm_service.py
    
    return{
        "response": ai_response
    }
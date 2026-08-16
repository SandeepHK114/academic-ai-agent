from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv
import shutil


#Why use ChromaDB, developer friendly, can run locally on your machine and is seamless with langchain 
load_dotenv()
API_KEY = os.getenv("API_KEY")

#DATA_PATH = "src/data/docs"
CHROMA_PATH = "chroma"

def create_database(file_path: str):
    generate_data_store(file_path)

#Saving chunks to ChromaDB
def generate_data_store(file_path: str):
    documents = load_doc(file_path)
    chunks = split_text(documents)
    save_to_chroma(chunks)

#Loading PDF into Document format
def load_doc(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

#Splitting document into chunks
def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 500,
        length_function = len,
        add_start_index = True
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} into {len(chunks)} chunks")

    return chunks

#Embedding chunks as vectors
def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    embeddings = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-2", api_key= API_KEY)

    db = Chroma.from_documents(
        chunks, embedding = embeddings, persist_directory=CHROMA_PATH
    )
    
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}")

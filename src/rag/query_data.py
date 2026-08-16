from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
CHROMA_PATH = "chroma"

def get_context(question: str) -> str:

    #Preparing DB

    embeddings = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-2", api_key= API_KEY)

    db = Chroma(persist_directory= CHROMA_PATH, embedding_function= embeddings)


    #returns a List of tuples that contain content and score as float: List[Tuple[Document,float]]
    results = db.similarity_search_with_relevance_scores(question, k=15)

    #checks to see if the returned List is empty or the scores are too low
    if len(results) == 0:
        print(f"Unable to find matching results.")
        return

    #Joining all the returned text into one string
    content_text = "\n\n ---\n\n".join([doc.page_content for doc, score in results])

    return content_text
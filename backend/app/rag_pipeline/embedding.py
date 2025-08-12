import os
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY is not set in the .env file.")


def get_embedding_function():
    """
    Initializes and returns the Cohere embedding model for the project.
    """
    return CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key=cohere_api_key)


def create_vector_store(documents, embedding_function):
    """
    Creates a FAISS vector store from the given documents and embedding function.
    Used for fast similarity searches.
    """
    if not documents:
        raise ValueError("Cannot create vector store from empty documents list.")
        
    print(f"Creating vector store from {len(documents)} document chunks...")
    
    vector_store = FAISS.from_documents(documents, embedding_function)
    
    print("Vector store created successfully.")
    return vector_store

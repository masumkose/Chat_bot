# In app/main.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .rag_pipeline.chunking import load_and_chunk_documents
from .rag_pipeline.embedding import get_embedding_function, create_vector_store
from .api import routes

# --- THE LIFESPAN MANAGER ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Starting RAG pipeline
    """
    print("Application starting: RAG pipeline starting...")
    
    # 1. Load and chunk documents
    documents = load_and_chunk_documents(data_path="./data")
    
    # 2. Get the embedding function
    embedding_function = get_embedding_function()
    
    # 3. Create the vector store and save it to the application's state
    vector_store = create_vector_store(documents, embedding_function)
    app.state.vector_store = vector_store

    print("RAG pipeline ready. Application is waiting for queries.")
    
    yield
    
    print("Application shutting down.")


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the LongevAI RAG Chatbot API"}

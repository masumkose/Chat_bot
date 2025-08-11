# In app/main.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import your modules for building the vector store
# You will need to create these functions in your rag_pipeline modules
# For example:
from .rag_pipeline.chunking import load_and_chunk_documents  # Assumes you have this function
from .rag_pipeline.embedding import get_embedding_function, create_vector_store  # Assumes you have these

# Import your router
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


# Initialize your FastAPI application with the lifespan manager
app = FastAPI(lifespan=lifespan)

# --- ADD CORS SETTINGS HERE ---
# Specify the address where your frontend is running (or "*" for all addresses).
origins = [
    "http://localhost:3000",  # Default address for Next.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# --- END OF CORS SETTINGS ---

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the LongevAI RAG Chatbot API"}

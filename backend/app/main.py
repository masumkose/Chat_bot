# In app/main.py

import os
import boto3
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .rag_pipeline.chunking import load_and_chunk_documents
from .rag_pipeline.embedding import get_embedding_function, create_vector_store
from .api import routes

# --- Helper function to download RAG data from S3 ---
def download_data_from_s3():
    """
    Downloads RAG source documents from a private S3 bucket if credentials are set.
    """
    print("Checking for data from S3...")
    
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    if not all([bucket_name, aws_access_key_id, aws_secret_access_key]):
        print("S3 environment variables not configured. Skipping S3 download.")
        return

    local_data_dir = "./data"
    os.makedirs(local_data_dir, exist_ok=True)
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        objects = response.get('Contents', [])
        
        if not objects:
            print(f"S3 bucket '{bucket_name}' is empty or inaccessible.")
            return

        print(f"Found {len(objects)} files in S3 bucket. Starting download to '{local_data_dir}'...")
        for obj in objects:
            file_key = obj['Key']
            if file_key.endswith('/'):
                continue
            
            local_file_path = os.path.join(local_data_dir, os.path.basename(file_key))
            print(f"Downloading s3://{bucket_name}/{file_key}...")
            s3_client.download_file(bucket_name, file_key, local_file_path)
            
        print("S3 download complete.")
    except Exception as e:
        print(f"An error occurred while downloading from S3: {e}")


# --- The LIFESPAN MANAGER ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    print("Application starting...")
    download_data_from_s3()
    
    print("RAG pipeline starting...")
    documents = load_and_chunk_documents(data_path="./data")
    embedding_function = get_embedding_function()
    vector_store = create_vector_store(documents, embedding_function)
    app.state.vector_store = vector_store

    print("RAG pipeline ready. Application is waiting for queries.")
    
    yield
    
    print("Application shutting down.")


app = FastAPI(lifespan=lifespan)

# --- THE FIX IS HERE: ADD THE CORS MIDDLEWARE ---
# Define the list of allowed origins
origins = [
    "http://localhost:3000",  # For local development
]

# Get the production domain from an environment variable
production_domain = os.getenv("DOMAIN_URL")

# If the environment variable exists and is not empty, add it to the list
if production_domain:
    print(f"Adding production domain to CORS origins: {production_domain}")
    origins.append(production_domain)

# Add the middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)
# ---------------------------------------------------

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Portfolio RAG Chatbot API"}

@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Simple health check endpoint to confirm the API is running.
    Used by the frontend to "wake up" the service on Render.
    """
    return {"status": "ok"}
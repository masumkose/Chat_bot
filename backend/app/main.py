# In app/main.py

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import your modules for building the vector store
# You will need to create these functions in your rag_pipeline modules
# For example:
from .rag_pipeline.chunking import load_and_chunk_documents # Assumes you have this function
from .rag_pipeline.embedding import get_embedding_function, create_vector_store # Assumes you have these

# Import your router
from .api import routes

# --- THE LIFESPAN MANAGER ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Uygulama  RAG pipeline' başlatr.
    """
    print("Uygulama başlyor: RAG pipeline' başlatlyor...")
    
    # 1. Dökümanları yükle ve parçala
    documents = load_and_chunk_documents(data_path="./data")
    
    # 2. Embedding fonksiyonunu al
    embedding_function = get_embedding_function()
    
    # 3. Vektör deposunu oluştur ve uygulamanın durumuna (state) kaydet
    vector_store = create_vector_store(documents, embedding_function)
    app.state.vector_store = vector_store
    
    print("RAG pipeline hazr. Uygulama sorgu bekliyor.")
    
    yield
    
    print("Uygulama kapanyor.")



# Initialize your FastAPI application with the lifespan manager
app = FastAPI(lifespan=lifespan)

# --- CORS AYARLARINI BURAYA EKLEYİN ---
# Frontend'in çalıştığı adresi (veya tüm adresler için "*") belirtin.
origins = [
    "http://localhost:3000", # Next.js'in varsayılan adresi
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Tüm metodlara (GET, POST, vb.) izin ver
    allow_headers=["*"], # Tüm başlıklara izin ver
)
# --- CORS AYARLARI BİTTİ ---

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the LongevAI RAG Chatbot API"}
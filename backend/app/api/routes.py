from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from ..rag_pipeline.retrieval import rerank_documents
from ..rag_pipeline.generation import generate_answer

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat(chat_request: ChatRequest, request: Request):
    try:
        vector_store = request.app.state.vector_store
        
        # 1. Retrieval
        retrieved_docs = vector_store.similarity_search(chat_request.query, k=10)
        
        # 2. Reranking
        reranked_docs = rerank_documents(chat_request.query, retrieved_docs)
        
        # 3. Generation
        answer = generate_answer(chat_request.query, reranked_docs)
        
        return {"answer": answer}
    except Exception as e:
        print(f"Hata /chat endpoint'inde: {e}")
        raise HTTPException(status_code=500, detail=str(e))
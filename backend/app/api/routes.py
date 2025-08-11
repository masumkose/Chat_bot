# routes.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any # <<< YENİ IMPORTLAR
from ..rag_pipeline.retrieval import rerank_documents
from ..rag_pipeline.generation import generate_answer
from fastapi.responses import StreamingResponse

router = APIRouter()

# ChatRequest modelini güncelliyoruz: artık bir 'query' değil, 'messages' dizisi bekliyor.
class ChatRequest(BaseModel):
    messages: List[Dict[str, Any]] # <<< DEĞİŞİKLİK BURADA

@router.post("/chat")
async def chat(chat_request: ChatRequest, request: Request):
    try:
        vector_store = request.app.state.vector_store
        
        # Son kullanıcı mesajının içeriğini alıyoruz.
        # RAG için sorgu olarak kullanılacak.
        last_user_message_content = ""
        for msg in reversed(chat_request.messages): # Sondan başa doğru arıyoruz
            if msg["role"] == "user":
                # AI SDK'nın gönderdiği 'content' string veya dizi olabilir.
                if isinstance(msg["content"], str):
                    last_user_message_content = msg["content"]
                elif isinstance(msg["content"], list):
                    for part in msg["content"]:
                        if part.get("type") == "text":
                            last_user_message_content = part.get("text", "")
                            break # Metin içeriğini bulur bulmaz döngüden çık
                break # Kullanıcı mesajını bulur bulmaz dış döngüden çık

        if not last_user_message_content:
            raise HTTPException(status_code=400, detail="No user message found to process.")

        # 1. Retrieval (Sorgu olarak son kullanıcı mesajını kullanıyoruz)
        retrieved_docs = vector_store.similarity_search(last_user_message_content, k=10)
        
        # 2. Reranking
        reranked_docs = rerank_documents(last_user_message_content, retrieved_docs)
        
        # 3. Generation (Artık tüm mesaj geçmişini gönderiyoruz)
        # generate_answer fonksiyonuna hem mesaj geçmişini hem de RAG dökümanlarını iletiyoruz.
        answer_generator = generate_answer(chat_request.messages, reranked_docs)
        
        # 4. Stream the response
        return StreamingResponse(answer_generator, media_type="text/plain")

    except Exception as e:
        print(f"Hata /chat endpoint'inde: {e}")
        raise HTTPException(status_code=500, detail=str(e))
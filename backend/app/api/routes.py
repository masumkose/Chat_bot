# routes.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any  # <<< NEW IMPORTS
from ..rag_pipeline.retrieval import rerank_documents
from ..rag_pipeline.generation import generate_answer
from fastapi.responses import StreamingResponse

router = APIRouter()

class ChatRequest(BaseModel):
    messages: List[Dict[str, Any]]

@router.post("/chat")
async def chat(chat_request: ChatRequest, request: Request):
    try:
        vector_store = request.app.state.vector_store
        
        last_user_message_content = ""
        for msg in reversed(chat_request.messages):
            if msg["role"] == "user":
                # The 'content' sent by the AI SDK can be a string or an array.
                if isinstance(msg["content"], str):
                    last_user_message_content = msg["content"]
                elif isinstance(msg["content"], list):
                    for part in msg["content"]:
                        if part.get("type") == "text":
                            last_user_message_content = part.get("text", "")
                            break  # Exit loop as soon as we find text content
                break  # Exit outer loop as soon as we find a user message

        if not last_user_message_content:
            raise HTTPException(status_code=400, detail="No user message found to process.")

        # 1. Retrieval (Use the last user message as the query)
        retrieved_docs = vector_store.similarity_search(last_user_message_content, k=10)
        
        # 2. Reranking
        reranked_docs = rerank_documents(last_user_message_content, retrieved_docs)
        
        # 3. Generation (Now we send the entire message history)
        # We send both the message history and the RAG documents to generate_answer.
        answer_generator = generate_answer(chat_request.messages, reranked_docs)
        
        # 4. Stream the response
        return StreamingResponse(answer_generator, media_type="text/plain")

    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

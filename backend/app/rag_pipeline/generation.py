import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List
from langchain_core.documents import Document

# .env dosyasını yükle
load_dotenv()

# .env dosyasından OpenAI API anahtarını al
# OPENAI_API_KEY="sizin_openai_api_anahtarınız"
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file.")

# OpenAI istemcisini başlat
client = OpenAI(api_key=openai_api_key)

def generate_answer(query: str, reranked_docs: List[Document]) -> str:
    """
    Kullanıcının sorusunu ve rerank edilmiş dökümanları kullanarak bir LLM ile cevap üretir.
    """
    # LLM'e verilecek olan context'i (bağlamı) oluştur
    context = "\n\n---\n\n".join([doc.page_content for doc in reranked_docs])
    
    # LLM'e gönderilecek olan prompt'u (istem) oluştur
    prompt = f"""
    You are an expert Question-Answering assistant. Your goal is to provide accurate and helpful answers based ONLY on the provided context.
    If the context does not contain the information needed to answer the question, say "I do not have enough information to answer this question."

    CONTEXT:
    {context}

    QUESTION:
    {query}

    ANSWER:
    """
    
    print("Generating answer with LLM...")

    # OpenAI API'sini çağır
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Proje gereksinimine uygun model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2, # Daha tutarlı cevaplar için düşük bir değer
    )
    
    answer = response.choices[0].message.content
    print("Answer generated successfully.")
    
    return answer
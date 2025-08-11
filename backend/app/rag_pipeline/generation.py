# generation.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any, Generator # <<< YENİ IMPORTLAR
from langchain_core.documents import Document

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY, .env dosyasında ayarlanmamış.")

client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

# Fonksiyonun imzasını güncelliyoruz: 'query' yerine 'messages' alıyor.
def generate_answer(messages: List[Dict[str, Any]], reranked_docs: List[Document]) -> Generator[str, None, None]:
    """
    Kullanıcının mesaj geçmişini ve yeniden sıralanmış dökümanları kullanarak LLM ile bir cevap üretir.
    Bu fonksiyon artık bir generator'dur ve cevabı parça parça yield eder.
    """
    context = "\n\n---\n\n".join([doc.page_content for doc in reranked_docs])

    # RAG bağlamını içeren bir sistem mesajı oluşturuyoruz.
    system_message_content = f"""
    You are an expert Question-Answering assistant.
    Your goal is to provide accurate and helpful answers based ONLY on the provided context.
    If the context does not contain the information needed to answer the question, say "I do not have enough information to answer this question."
    CONTEXT:
    {context}
    """

    # Gemini'ye gönderilecek mesaj listesini hazırlıyoruz.
    # İlk olarak RAG bağlamını sistem mesajı olarak ekliyoruz.
    gemini_messages = [{"role": "system", "content": system_message_content}]

    # Frontend'den gelen mesaj geçmişini Gemini'nin anlayacağı formata dönüştürüyoruz.
    # AI SDK'nın 'content' alanı string veya bir liste olabilir (multimodal için).
    # Biz sadece metin içeriğini alacağız.
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        
        # Gemini'nin OpenAI uyumluluk katmanı genellikle 'user' ve 'assistant' rollerini bekler.
        gemini_role = "user" if role == "user" else "assistant" # 'model' yerine 'assistant' kullanıyoruz.

        formatted_content = ""
        if isinstance(content, str):
            formatted_content = content
        elif isinstance(content, list): # Multimodal içerik için
            for part in content:
                if part.get("type") == "text":
                    formatted_content += part.get("text", "")
                # Eğer görsel veya başka tür içerikler de desteklenecekse,
                # burada ilgili formatlamaları yapmanız gerekebilir.
                # OpenAI client'ın Gemini ile multimodal desteği API tarafında kısıtlı olabilir.
                # Şimdilik sadece text'i ele alıyoruz.
        
        # Boş mesajları veya sadece boşluk içeren mesajları eklememek için kontrol
        if formatted_content.strip():
            gemini_messages.append({"role": gemini_role, "content": formatted_content})
        
    print("Generating answer with Gemini (streaming) using full message history...")
    
    try:
        # OpenAI API'sini stream=True parametresi ile çağırıyoruz
        stream = client.chat.completions.create(
            model="gemini-2.5-flash", # "gemini-pro" veya "gemini-1.5-flash" kullanın.
                                       # ':generateContent' kısmı OpenAI uyumluluk katmanında genellikle gerekmez.
            messages=gemini_messages,  # <<< Tüm mesaj geçmişini gönderiyoruz
            temperature=0.2,
            stream=True,
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
                yield content

    except Exception as e:
        print(f"Gemini API çağrısı sırasında hata: {e}")
        yield "Cevap üretilirken bir hata oluştu."
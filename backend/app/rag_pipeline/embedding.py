import os
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS

# .env dosyasındaki environment variables'ı yükle
load_dotenv()

# API anahtarının .env dosyasında olduğundan emin olun
# COHERE_API_KEY="sizin_cohere_api_anahtarınız"
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY is not set in the .env file.")


def get_embedding_function():
    """
    Proje gereksinimlerine uygun olarak Cohere embedding modelini başlatır ve döndürür.
    """
    # model='embed-english-v3.0' veya 'embed-english-light-v3.0' gibi modelleri kullanabilirsiniz.
    return CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key=cohere_api_key)


def create_vector_store(documents, embedding_function):
    """
    Verilen dökümanları ve embedding fonksiyonunu kullanarak bir FAISS vektör deposu oluşturur.
    Bu depo, hızlı benzerlik aramaları için kullanılır.
    """
    if not documents:
        raise ValueError("Cannot create vector store from empty documents list.")
        
    print(f"Creating vector store from {len(documents)} document chunks...")
    
    # LangChain'in FAISS entegrasyonunu kullanarak vektör deposunu oluştur
    vector_store = FAISS.from_documents(documents, embedding_function)
    
    print("Vector store created successfully.")
    return vector_store
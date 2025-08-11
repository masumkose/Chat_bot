import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List
from langchain_core.documents import Document

# .env load the env file
load_dotenv()

# .env take the api key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY, .env dosyasında ayarlanmamış.")

# OpenAI for Gemini API
client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def generate_answer(query: str, reranked_docs: List[Document]) -> str:
    """
    Generates an answer using the user's question and the re-ranked documents with an LLM.
    (The inside of this function remains the same)
    """
    # context
    context = "\n\n---\n\n".join([doc.page_content for doc in reranked_docs])

    # To send LLM'e create a promt
    prompt = f"""
    You are an expert Question-Answering assistant. Your goal is to provide accurate and helpful answers based ONLY on the provided context.
    If the context does not contain the information needed to answer the question, say "I do not have enough information to answer this question."

    CONTEXT:
    {context}

    QUESTION:
    {query}

    ANSWER:
    """

    print("Generating answer with Gemini via OpenAI library...")

    # OpenAI API call, Call the gemini api
    response = client.chat.completions.create(
        model="gemini-2.5-flash",  # gemini.2.5 flash
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content
    print("Answer generated successfully.")

    return answer
# generation.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any, Generator  # <<< NEW IMPORTS
from langchain_core.documents import Document

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta"
)


def generate_answer(messages: List[Dict[str, Any]], reranked_docs: List[Document]) -> Generator[str, None, None]:
    """
    Generates an answer using the user's message history and reranked documents.
    This function is a generator and yields the answer in chunks.
    """
    context = "\n\n---\n\n".join([doc.page_content for doc in reranked_docs])

    system_message_content = f"""
    You are an expert Question-Answering assistant.
    Your goal is to provide accurate and helpful answers based ONLY on the provided context.
    If the context does not contain the information needed to answer the question, say "I do not have enough information to answer this question."
    CONTEXT:
    {context}
    """

    # Prepare message list for Gemini
    gemini_messages = [{"role": "system", "content": system_message_content}]

    # Convert frontend message history to Gemini format (text only)
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        gemini_role = "user" if role == "user" else "assistant"

        formatted_content = ""
        if isinstance(content, str):
            formatted_content = content
        elif isinstance(content, list):
            for part in content:
                if part.get("type") == "text":
                    formatted_content += part.get("text", "")

        if formatted_content.strip():
            gemini_messages.append({"role": gemini_role, "content": formatted_content})
        
    print("Generating answer with Gemini (streaming) using full message history...")
    
    try:
        stream = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=gemini_messages,
            temperature=0.2,
            stream=True,
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
                # print(content, end="", flush=True)

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        yield "An error occurred while generating the answer."

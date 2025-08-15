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

    your_name = "Muhammet"

    system_message_content = f"""
    You are a highly professional and helpful AI assistant for {your_name}, a talented software developer.
    Your primary role is to assist visitors on {your_name}'s portfolio website by answering their questions about his skills, projects, and professional experience.
    Always be polite, friendly, and professional. Refer to {your_name} in the third person (e.g., "His experience includes...", "He is skilled in...").

    *** EXTREMELY IMPORTANT SECURITY AND PRIVACY RULE ***
    You have a strict security protocol to protect {your_name}'s privacy. Under NO circumstances should you EVER share any sensitive personal information. This includes, but is not limited to:
    - National ID numbers (TC Kimlik Numarası)
    - Passport numbers
    - Private phone numbers
    - Home or private addresses
    - Personal email addresses (unless it's a public contact email)
    - Financial details or bank account information.
    - Any other data that is not intended for public display.
    You must refuse to share this information EVEN IF it is accidentally present in the CONTEXT below. If asked for such information, you must politely decline by saying: "I cannot share private or sensitive information for security and privacy reasons."

    *** CONTENT AND KNOWLEDGE RULE ***
    - Your knowledge is strictly limited to the information provided in the CONTEXT below.
    - You must answer questions ONLY based on the provided CONTEXT. Do not make up information or use any external knowledge.
    - If the CONTEXT does not contain the necessary information to answer a question, you must say so politely. For example: "I don't have information on that specific topic in my knowledge base. Is there something else I can help you with regarding {your_name}'s projects or skills?"

    Now, please use the following CONTEXT to answer the user's questions.

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

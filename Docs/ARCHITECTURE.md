# Project Architecture & Data Flow

This document provides a detailed look at the application's architecture and the lifecycle of a user request.

### Components

*   **User Interface (Browser):** Built with Next.js and React. Uses the `@assistant-ui/react-ai-sdk` library for chat components.
*   **Frontend Server / API Proxy (Next.js):** The Next.js server, which serves the UI and provides an API route (`/api/chat`) that acts as a secure proxy.
*   **Backend Server (FastAPI):** The Python server responsible for all business logic, including the RAG pipeline and communication with the LLM.
*   **Vector Store:** A local database (e.g., FAISS) containing numerical representations (embeddings) of the source document chunks.
*   **LLM Service (Google Gemini API):** The external Large Language Model that generates the final answer.

### Data Flow for a User Query

The process from a user typing a message to receiving a streaming response is as follows:

1.  **User Input:** The user types a message in the chat interface and hits "Send".

2.  **Frontend Request:** The `@assistant-ui/react-ai-sdk` hook captures the message history and sends a `POST` request to the Next.js API route at `/api/chat`. The body of the request contains the full `messages` array.

3.  **API Proxy Forwarding:**
    *   The Next.js `/api/chat` route receives the request.
    *   It extracts the `messages` array from the JSON body.
    *   It then makes a new `POST` request, forwarding the *exact same* `messages` array to the Python backend at `http://localhost:8000/chat`.

4.  **Backend Processing (RAG Pipeline):**
    *   The FastAPI server receives the request at its `/chat` endpoint.
    *   **Query Extraction:** It inspects the `messages` array to find the content of the most recent user message. This content is used as the query for the RAG pipeline.
    *   **Retrieval:** The query is used to perform a similarity search on the Vector Store. The top `k` most similar document chunks are retrieved.
    *   **Reranking:** The retrieved chunks are passed to a reranker model, which re-orders them based on their direct relevance to the user's query. This improves the signal-to-noise ratio.

5.  **LLM Communication:**
    *   **Prompt Construction:** A new prompt is constructed. It includes a system message that instructs the model on how to behave, the high-quality context from the reranked documents, and the full conversation history.
    *   **API Call:** The backend uses the `openai` client to make a `POST` request to the Gemini API, sending the constructed prompt and enabling `stream=True`.

6.  **Streaming Response (Return Path):**
    *   **Gemini -> Backend:** The Gemini API starts sending back the response token by token (or in small chunks). The FastAPI backend's `generate_answer` function `yield`s each chunk as it arrives. FastAPI's `StreamingResponse` sends these raw text chunks back to the Next.js API Proxy.
    *   **Backend -> API Proxy:** The Next.js API Proxy receives the raw text stream.
    *   **Stream Transformation:** The proxy's `toVercelAiStream` function intercepts each raw text chunk (e.g., `" The"`). It transforms it into the format expected by the Vercel AI SDK (e.g., `0:" The"\n`).
    *   **API Proxy -> UI:** The transformed, correctly formatted stream is sent back to the user's browser.

7.  **UI Rendering:** The `@assistant-ui/react-ai-sdk` hook receives the formatted stream, decodes it, and renders the assistant's response word-by-word in the chat window, providing a real-time, streaming user experience.
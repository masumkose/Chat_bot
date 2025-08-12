# RAG-Powered Financial Investment Assistant

**Project for Elio Verhoef**

## 1. Project Overview & Chosen Topic

This project is a full-stack, streaming-capable chat assistant designed to answer questions based on a provided set of documents. It uses a Retrieval-Augmented Generation (RAG) pipeline to provide accurate, context-aware answers.

*   **Chosen Topic:** Financial Investment Principles
*   **Document Sources:** The knowledge base for this assistant was built from the following sources:
    *   `Value Investing, a Modern Approach, Yuqin Guo`
    *   `The Eight Principles of Value Investing By Scott Clemons and Michael Kim October, 2013`
    *   `FINANCING THE UNITED NATIONS, Max-Otto Baumann, Sebastian Haug April 2024`
    *   `Gemini produces txt file about finance terms.`

The assistant leverages a Python/FastAPI backend for the RAG logic and a Next.js frontend for a reactive user interface, with real-time streaming of responses from the Google Gemini LLM.

---

## 2. Technical Architecture

The application is split into two main components:

1.  **Frontend (Next.js & Vercel AI SDK):** A user-friendly chat interface that handles user input and renders the streaming responses from the backend.
2.  **Backend (Python, FastAPI & Gemini):** A robust API that performs the core RAG logic:
    *   Receives the conversation history from the frontend.
    *   Performs semantic search on a vector database to find relevant document chunks.
    *   Re-ranks the retrieved documents for improved context quality.
    *   Constructs a detailed prompt with the user's question and the retrieved context.
    *   Streams the response from the Google Gemini API back to the frontend.

For a more detailed data flow diagram, please see **`docs/ARCHITECTURE.md`**.

---

## 3. Setup and Installation Instructions

Please follow these steps to set up and run the project locally.

### Prerequisites

*   **Python 3.9+** and `pip`
*   **Node.js 18+** and `npm` (or `yarn`)
*   A valid **Google Gemini API Key**
*   A valid **Cohere API Key**

### Step 1: Backend Setup

First, set up and run the Python backend server.

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    *   Create a `.env` file in the `backend` directory.
    *   Copy the contents of `.env.example` into it and add your Gemini API key.

    **File: `backend/.env`**
    ```
    GEMINI_API_KEY="your-google-gemini-api-key-here"
    COHERE_API_KEY="your-cohere-api-key-here"
    ```
5.  **Run the Backend Server:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    The backend is now running on `http://localhost:8000`.

6.  **Automatic Ingestion:**
    *   The **first time** you run this command, the server will detect that no vector store exists.
    *   It will automatically read the documents from the `backend/data` directory, process them, and build the vector database. This may take a few moments depending on the number and size of your documents.
    *   On all subsequent startups, the server will load the existing vector store instantly.


### Step 2: Frontend Setup

Now, set up and run the Next.js frontend in a separate terminal.

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Configure Environment Variables:**
    *   Create a `.env.local` file in the `frontend` directory.
    *   This file tells the frontend where the backend is running.

    **File: `frontend/.env.local`**
    ```
    BACKEND_URL="http://localhost:8000"
    ```

4.  **Run the Frontend Development Server:**
    ```bash
    npm run dev
    ```

### Step 3: Usage

Open your web browser and navigate to **`http://localhost:3000`**. You can now start chatting with the assistant.

---

## 4. Assumptions & Trade-offs

During development, several decisions were made:

*   **Assumption: Local Vector Store:**
    *   I have used a local file-based vector store (e.g., FAISS or ChromaDB) for simplicity and to avoid requiring a separate database server.
    *   **Trade-off:** This is great for local development but is not suitable for a production environment, which would require a persistent, scalable vector database solution.

*   **Assumption: Gemini via OpenAI SDK:**
    *   I am using the `openai` Python library to interact with the Gemini API via its OpenAI compatibility endpoint.
    *   **Trade-off:** While this provides a familiar interface, it might not support all of Gemini's native features (like advanced function calling or specific safety settings). Using the native `google-generativeai` library would offer more control at the cost of a different implementation pattern.

*   **Trade-off: API Proxy Route in Next.js:**
    *   The frontend does not call the Python backend directly. Instead, it calls a Next.js API route (`/api/chat`) which then "proxies" the request to the Python backend.
    *   **Pro:** This is a best practice for security. It hides the backend's architecture and URL from the public-facing client and protects against CORS issues. It also allows for frontend-side transformation of the data stream, as was necessary here.
    *   **Con:** This adds one extra network hop, which introduces a minuscule amount of latency. For this application, the trade-off is well worth it.

*   **Trade-off: Reranking Step:**
    *   The RAG pipeline includes a reranking step after the initial document retrieval.
    *   **Pro:** This significantly improves the quality of the context provided to the LLM by pushing the most relevant documents to the top, leading to more accurate answers.
    *   **Con:** Reranking adds a small computational cost and latency to each request.
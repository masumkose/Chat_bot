# Project Architecture & Data Flow

This document provides a detailed look at the application's architecture and the lifecycle of a user request.

### Component Breakdown

1.  **Frontend (Deployed on Vercel)**
    *   **Framework:** Next.js with the App Router.
    *   **Root Directory:** `frontend/`
    *   **Key Responsibilities:**
        *   Serving the static portfolio content and UI components.
        *   Dynamically fetching and rendering public projects from the GitHub API in a Server Component (`frontend/app/page.tsx`).
        *   Providing a real-time chat interface using the `assistant-ui` library.
        *   Proxying all chat requests through a dedicated API Route (`frontend/app/api/chat/route.ts`) to the backend. This is a security best practice that hides the backend's URL from the client and handles potential CORS issues.

2.  **Backend (Deployed on Render)**
    *   **Framework:** FastAPI (Python), running in a Docker container.
    *   **Root Directory:** `backend/`
    *   **Key Responsibilities:**
        *   On startup, securely downloading the latest RAG documents from a private AWS S3 bucket.
        *   Building a vector store in memory from these documents (this is the core of the RAG pipeline).
        *   Exposing a single `/chat` endpoint to handle incoming conversation history from the Vercel proxy.
        *   Constructing a detailed prompt using the user's query and context retrieved from the vector store.
        *   Streaming the final response from the Google Gemini API back to the frontend proxy.

---

### Request Lifecycle for an AI Chat Message

The end-to-end data flow for a user's chat message is visualized below. This process is designed for real-time, streaming responses.

```mermaid
sequenceDiagram
    participant Browser as User's Browser
    participant Vercel as Vercel API Route
    participant Render as Render Backend
    participant Gemini as Gemini API

    Browser->>+Vercel: (1) POST /api/chat with message history
    Vercel->>+Render: (2) Forwards request to BACKEND_URL
    Render->>Render: (3) Performs RAG Pipeline (Vector Search)
    Render->>+Gemini: (4) Streams final prompt with context
    Gemini-->>-Render: (4) Streams response back
    Render-->>-Vercel: (4) Forwards streamed response
    Vercel-->>-Browser: (5) Streams formatted response to UI


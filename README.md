# AI-Powered Portfolio & Personal Chat Assistant

**A full-stack, AI-driven portfolio website built by Muhammet Köse.**

---

### 🚀 Live Demo

**Interact with the deployed application here:**

**[masum-kose-portfolio.vercel.app](https://masum-kose-portfolio.vercel.app/)** <!-- <<< IMPORTANT: Replace with your final custom domain or .vercel.app URL -->

---

## 1. Project Overview

This project is a modern, full-stack portfolio website designed to showcase my skills and projects. It features a unique, personalized AI assistant that acts as an interactive "living resume."

The assistant uses a **Retrieval-Augmented Generation (RAG)** pipeline to answer questions about my professional background, technical skills, and academic history. The knowledge base for this pipeline is built from a private collection of my personal documents (resumes, certificates, etc.), which are securely stored and managed.

## 2. Key Features

*   **Serverless Deployment:** The entire application is deployed on a modern serverless infrastructure (Vercel & Render), ensuring high availability and scalability with zero server maintenance.
*   **Containerized Backend:** The Python backend is fully containerized with Docker, making it portable, reproducible, and easy to deploy.
*   **Real-time Streaming:** The AI assistant streams responses token-by-token from the Google Gemini API for a highly interactive and engaging user experience.
*   **Secure RAG Pipeline:** Private source documents are securely fetched from a private AWS S3 bucket during the backend's startup, ensuring they are never exposed in the codebase or version control.
*   **Dynamic Project Showcase:** The portfolio section dynamically fetches and displays all of my public projects directly from the GitHub API, ensuring it's always up-to-date.

## 3. Tech Stack

| Component     | Technology                                                 |
| :------------ | :--------------------------------------------------------- |
| **Frontend**  | Next.js, React, TypeScript, Tailwind CSS, Assistant UI     |
| **Backend**   | Python, FastAPI, LangChain, Google Gemini                  |
| **Deployment**| Vercel (Frontend), Render (Backend), Docker                |
| **Data Storage**| AWS S3 (for private RAG documents)                         |

---

## 4. Architecture

The application uses a decoupled frontend/backend architecture, a modern standard for creating scalable and maintainable web applications.

For a more detailed breakdown of the data flow, see the **`Docs/ARCHITECTURE.md`** file.

---

## 5. Cloud Deployment (Vercel & Render)

This project is designed for a streamlined, Git-based deployment workflow.

### Backend Setup (Render)

1.  Create a new **Web Service** on Render and connect this GitHub repository.
2.  Set the **Environment** to **`Docker`**.
3.  Set the **Root Directory** to **`backend`**. This tells Render where to find the `Dockerfile`.
4.  Add the following **Environment Variables** in the Render dashboard to provide the necessary secrets:
    *   `DOMAIN_URL`
    *   `GEMINI_API_KEY`
    *   `COHERE_API_KEY`
    *   `AWS_S3_BUCKET_NAME`
    *   `AWS_ACCESS_KEY_ID`
    *   `AWS_SECRET_ACCESS_KEY`

### Frontend Setup (Vercel)

1.  Create a new **Project** on Vercel and import this GitHub repository.
2.  Set the **Root Directory** in the project settings to **`frontend`**.
3.  Add the following **Environment Variable** in the Vercel dashboard:
    *   `BACKEND_URL`: The public URL of the deployed backend service from Render.
4.  Pushing to the `master`/`main` branch will automatically trigger new deployments on both services.

---

## 6. Local Development

The entire application stack can be run locally using Docker Compose for a consistent development environment.

### Prerequisites
*   Docker & Docker Compose
*   Git

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/masumkose/portfolio-website.git
    cd portfolio-website
    ```

2.  **Create Environment Files:**
    *   In the `backend` folder, create a `.env` file and add     
        `DOMAIN_URL=...`
        `GEMINI_API_KEY=...`
        `COHERE_API_KEY=...`
        `AWS_S3_BUCKET_NAME=...`
        `AWS_ACCESS_KEY_ID=...`
        `AWS_SECRET_ACCESS_KEY=...`
    *   In the `frontend` folder, create a `.env.local` file and add 
        `BACKEND_URL=http://backend:8000`
        `NEXT_PUBLIC_FORMSPREE_URL=...`
        `NEXT_PUBLIC_BACKEND_URL=...`

3.  **Run the application:**
    ```bash
    docker-compose up --build
    ```
    or use make up 
    check for more details in the Makefile
4.  Access the frontend at `http://localhost:3000`.

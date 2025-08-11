from langchain.docstore.document import Document
from langchain_cohere import CohereRerank
from ..core.config import settings

def rerank_documents(query: str, retrieved_docs: list[Document]):
    """Reranks retrieved documents using Cohere for improved relevance."""
    reranker = CohereRerank(cohere_api_key=settings.COHERE_API_KEY, model="rerank-english-v3.0", top_n=5)
    return reranker.compress_documents(documents=retrieved_docs, query=query)
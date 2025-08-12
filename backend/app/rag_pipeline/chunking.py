from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader

def load_and_chunk_documents(data_path: str) -> List[Document]:
    print(f"Loading documents from: {data_path}...")

    documents = []

    # Load TXT files
    txt_loader = DirectoryLoader(
        data_path,
        glob="**/*.txt",
        loader_cls=TextLoader,
        use_multithreading=True,
        show_progress=True,
    )
    documents.extend(txt_loader.load())

    # Load PDF files
    pdf_loader = DirectoryLoader(
        data_path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        use_multithreading=True,
        show_progress=True,
    )
    documents.extend(pdf_loader.load())

    if not documents:
        raise ValueError(f"No documents found in {data_path}. Please add .txt or .pdf files.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunked_documents = text_splitter.split_documents(documents)

    print(f"Loaded {len(documents)} documents and split into {len(chunked_documents)} chunks.")
    return chunked_documents

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document

# LÜTFEN FONKSİYON TANIMININ BU ŞEKİLDE OLDUĞUNDAN EMİN OLUN
# 'data_path: str' ARGÜMANINI KABUL ETMELİDİR
def load_and_chunk_documents(data_path: str) -> List[Document]:
    """
    Belirtilen klasördeki dökümanları yükler ve RAG için uygun parçalara (chunk) ayırır.
    """
    print(f"Dökümanlar yükleniyor: {data_path}...")
    
    # use_multithreading=True, birden fazla dosya varsa işlemi hızlandırabilir
    loader = DirectoryLoader(
        data_path,
        glob="**/*.txt",
        loader_cls=TextLoader,
        use_multithreading=True,
        show_progress=True,
    )
    documents = loader.load()
    
    if not documents:
        raise ValueError(f"{data_path} içinde hiç döküman bulunamadı. Lütfen .txt dosyaları ekleyin.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunked_documents = text_splitter.split_documents(documents)
    
    print(f"{len(documents)} döküman yüklendi ve {len(chunked_documents)} parçaya ayrıldı.")
    return chunked_documents
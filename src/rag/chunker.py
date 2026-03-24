from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import settings


def chunk_text(text: str, metadata: dict | None = None) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk, metadata=metadata or {}) for chunk in chunks]


def chunk_documents(docs: list[dict]) -> list[Document]:
    all_chunks = []
    for doc in docs:
        metadata = {
            "source_url": doc.get("url", ""),
            "title": doc.get("title", ""),
            "timestamp": doc.get("timestamp", ""),
        }
        chunks = chunk_text(doc.get("content", ""), metadata=metadata)
        all_chunks.extend(chunks)
    return all_chunks

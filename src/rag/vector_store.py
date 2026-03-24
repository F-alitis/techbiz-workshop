from langchain_chroma import Chroma
from langchain_core.documents import Document

from config.settings import settings
from src.rag.embeddings import get_embeddings


def get_vector_store() -> Chroma:
    return Chroma(
        collection_name="nbg_docs",
        persist_directory=settings.vector_store_path,
        embedding_function=get_embeddings(),
    )


def add_documents(docs: list[Document]) -> None:
    store = get_vector_store()
    store.add_documents(docs)


def search(query: str, k: int = 5) -> list[Document]:
    store = get_vector_store()
    return store.similarity_search(query, k=k)


def get_collection_stats() -> dict:
    store = get_vector_store()
    collection = store._collection
    return {"count": collection.count()}

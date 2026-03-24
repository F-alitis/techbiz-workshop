from langchain_core.tools import tool
from src.rag.vector_store import search


@tool
def search_nbg_knowledge_base(query: str) -> str:
    """Search the pre-indexed NBG banking knowledge base.
    Use for: products, services, rates, general banking info.

    Args:
        query: User's question about NBG banking

    Returns:
        Relevant context from the knowledge base
    """
    results = search(query, k=5)
    if not results:
        return "No relevant information found in the knowledge base."

    context_parts = []
    for doc in results:
        source = doc.metadata.get("source_url", "unknown")
        context_parts.append(f"[Source: {source}]\n{doc.page_content}")

    return "\n\n---\n\n".join(context_parts)

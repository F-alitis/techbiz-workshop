from langchain_core.messages import AIMessage
from src.agent.state import AgentState
from src.agent.prompts import CLASSIFICATION_PROMPT, GENERATION_PROMPT
from src.agent.llm import ask_llm
from src.tools.rag_retrieval import search_nbg_knowledge_base
from src.tools.live_scraper import scrape_nbg_page
from config.settings import settings


def classify_query_node(state: AgentState) -> dict:
    """Classify the user query to determine routing.

    TODO: Implement during live demo
    - Use ask_llm() to classify as "rag", "scrape", or "both"
    - Use CLASSIFICATION_PROMPT with the user's query and available scrape URLs
    - Parse the LLM response to extract the classification and target scrape URL
    """
    # Extract user query from the last message
    messages = state.get("messages", [])
    user_query = messages[-1].content if messages else ""
    # Placeholder: always route to RAG
    return {"user_query": user_query, "next_action": "rag", "scrape_url": settings.nbg_scrape_urls[0], "tool_calls": 0}


def retrieve_from_rag_node(state: AgentState) -> dict:
    """Search the ChromaDB knowledge base for relevant context."""
    query = state.get("user_query", "")
    try:
        context = search_nbg_knowledge_base.invoke(query)
    except Exception as e:
        context = f"RAG retrieval failed: {e}"
    return {"rag_context": context, "tool_calls": state.get("tool_calls", 0) + 1}


def scrape_live_node(state: AgentState) -> dict:
    """Scrape live content from NBG website."""
    url = state.get("scrape_url", settings.nbg_scrape_urls[0])
    try:
        content = scrape_nbg_page.invoke(url)
    except Exception as e:
        content = f"Live scraping failed: {e}"
    return {"live_content": content, "tool_calls": state.get("tool_calls", 0) + 1}


def generate_answer_node(state: AgentState) -> dict:
    """Generate the final answer using retrieved context.

    TODO: Implement during live demo
    - Use ask_llm() with GENERATION_PROMPT
    - Inject rag_context and live_content into the prompt
    - Return the generated answer
    """
    # Placeholder response
    context = state.get("rag_context") or "No context available"
    return {
        "final_answer": f"[Demo placeholder] Based on available context:\n\n{context[:500]}...\n\n_Implement generate_answer_node during live demo for full functionality._",
        "messages": [AIMessage(content="Placeholder response generated")],
    }

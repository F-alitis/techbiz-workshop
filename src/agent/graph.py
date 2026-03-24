from langgraph.graph import StateGraph, END
from src.agent.state import AgentState, InputState
from src.agent.nodes import (
    classify_query_node,
    retrieve_from_rag_node,
    scrape_live_node,
    generate_answer_node,
)


def route_query(state: AgentState) -> str:
    """Route based on classification result."""
    return state.get("next_action", "rag")


def build_graph():
    workflow = StateGraph(AgentState, input=InputState)

    # Add nodes
    workflow.add_node("classify_query", classify_query_node)
    workflow.add_node("retrieve_from_rag", retrieve_from_rag_node)
    workflow.add_node("scrape_live", scrape_live_node)
    workflow.add_node("generate_answer", generate_answer_node)

    # Entry point
    workflow.set_entry_point("classify_query")

    # Conditional routing from classify_query
    workflow.add_conditional_edges(
        "classify_query",
        route_query,
        {
            "rag": "retrieve_from_rag",
            "scrape": "scrape_live",
            "both": "retrieve_from_rag",
        },
    )

    # After RAG retrieval, check if we also need scraping
    def after_rag(state: AgentState) -> str:
        if state.get("next_action") == "both" and state.get("tool_calls", 0) < 2:
            return "scrape_live"
        return "generate_answer"

    workflow.add_conditional_edges(
        "retrieve_from_rag",
        after_rag,
        {
            "scrape_live": "scrape_live",
            "generate_answer": "generate_answer",
        },
    )

    # After scraping, always generate answer
    workflow.add_edge("scrape_live", "generate_answer")

    # After generating answer, end
    workflow.add_edge("generate_answer", END)

    return workflow.compile()


# Compile the graph
graph = build_graph()

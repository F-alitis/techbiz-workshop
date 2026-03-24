from src.agent.state import AgentState
from langchain_core.messages import HumanMessage


def test_agent_state_creation():
    state: AgentState = {
        "messages": [HumanMessage(content="test")],
        "user_query": "test query",
        "rag_context": None,
        "live_content": None,
        "next_action": "rag",
        "final_answer": None,
        "tool_calls": 0,
    }
    assert state["user_query"] == "test query"
    assert state["next_action"] == "rag"
    assert len(state["messages"]) == 1


def test_agent_state_with_context():
    state: AgentState = {
        "messages": [],
        "user_query": "What cards does NBG offer?",
        "rag_context": "NBG offers Visa and Mastercard",
        "live_content": None,
        "next_action": "rag",
        "final_answer": "NBG offers Visa and Mastercard cards.",
        "tool_calls": 1,
    }
    assert state["rag_context"] is not None
    assert state["final_answer"] is not None

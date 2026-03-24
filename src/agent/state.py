from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class InputState(TypedDict):
    """What the user provides — shown in Studio."""
    messages: Annotated[Sequence[BaseMessage], add_messages]


class AgentState(InputState, total=False):
    """Full internal state — not shown in Studio input."""
    user_query: str
    rag_context: str
    live_content: str
    next_action: str
    final_answer: str
    tool_calls: int

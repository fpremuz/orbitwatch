from langgraph.graph import StateGraph
from langgraph.graph import END

from app.ai.agents.state import AgentState
from app.ai.agents.nodes import (
    retrieve_context,
    generate_answer,
)


builder = StateGraph(AgentState)

builder.add_node(
    "retrieve",
    retrieve_context,
)

builder.add_node(
    "generate",
    generate_answer,
)

builder.set_entry_point(
    "retrieve"
)

builder.add_edge(
    "retrieve",
    "generate",
)

builder.add_edge(
    "generate",
    END,
)

graph = builder.compile()
from langgraph.graph import END
from langgraph.graph import StateGraph

from app.ai.agents.nodes import (
    classify_request,
    retrieve_context,
    execute_tool,
    generate_answer,
)
from app.ai.agents.state import AgentState


builder = StateGraph(AgentState)

builder.add_node(
    "route",
    classify_request,
)

builder.add_node(
    "retrieve",
    retrieve_context,
)

builder.add_node(
    "tool",
    execute_tool,
)

builder.add_node(
    "generate",
    generate_answer,
)

builder.set_entry_point("route")


def route(state):

    if state["use_tool"]:
        return "tool"

    return "retrieve"


builder.add_conditional_edges(
    "route",
    route,
)

builder.add_edge(
    "retrieve",
    "generate",
)

builder.add_edge(
    "tool",
    "generate",
)

builder.add_edge(
    "generate",
    END,
)

graph = builder.compile()
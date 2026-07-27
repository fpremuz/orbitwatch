from langgraph.graph import StateGraph
from langgraph.graph import END

from app.ai.agents.state import AgentState
from app.ai.agents.nodes import (
    decide_route,
    retrieve_context,
    generate_answer,
    direct_answer,
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

builder.add_node(
    "direct",
    direct_answer,
)

builder.set_conditional_entry_point(
    decide_route,
    {
        "retrieve": "retrieve",
        "direct": "direct",
    },
)

builder.add_edge(
    "retrieve",
    "generate",
)

builder.add_edge(
    "generate",
    END,
)

builder.add_edge(
    "direct",
    END,
)

graph = builder.compile()
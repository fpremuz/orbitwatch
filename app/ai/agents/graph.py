from langgraph.graph import END
from langgraph.graph import StateGraph

from app.ai.agents.nodes import (
    direct_answer,
    generate_answer,
    retrieve_context,
)
from app.ai.agents.router import route_question
from app.ai.agents.state import AgentState

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
    route_question,
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
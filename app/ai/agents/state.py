from typing import Literal
from typing import TypedDict


Decision = Literal[
    "retrieve",
    "tool",
    "both",
    "direct",
]


class AgentState(TypedDict):
    question: str

    history: str

    context: str

    tool_output: str

    decision: Decision

    answer: str
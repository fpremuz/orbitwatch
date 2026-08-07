from typing import TypedDict


class AgentState(TypedDict):
    question: str

    history: str

    decision: str

    selected_tool: str

    context: str

    tool_output: str

    answer: str
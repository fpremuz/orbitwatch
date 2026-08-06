from typing import TypedDict


class AgentState(TypedDict):
    question: str

    history: str

    context: str

    tool_output: str

    use_tool: bool

    answer: str
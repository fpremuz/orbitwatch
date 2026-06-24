from typing import TypedDict


class AgentState(TypedDict):
    question: str
    history: str

    context: str

    answer: str
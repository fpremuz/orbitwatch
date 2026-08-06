from typing import Literal


TELEMETRY_KEYWORDS = [
    "satellite",
    "telemetry",
    "temperature",
    "battery",
    "orbit",
    "velocity",
    "altitude",
    "signal",
    "communication",
    "anomaly",
    "ground station",
]

TOOL_KEYWORDS = [
    "alert",
    "alerts",
    "critical",
    "warning",
    "latest",
    "recent",
]


def route_question(state) -> Literal["retrieve", "tool", "direct"]:

    question = state["question"].lower()

    if any(keyword in question for keyword in TOOL_KEYWORDS):
        return "tool"

    if any(keyword in question for keyword in TELEMETRY_KEYWORDS):
        return "retrieve"

    return "direct"
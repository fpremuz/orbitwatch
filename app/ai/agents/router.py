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


def route_question(state) -> Literal["retrieve", "direct"]:

    question = state["question"].lower()

    for keyword in TELEMETRY_KEYWORDS:
        if keyword in question:
            return "retrieve"

    return "direct"
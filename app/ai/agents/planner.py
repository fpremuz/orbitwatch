from typing import Literal


Decision = Literal[
    "retrieve",
    "tool",
    "both",
    "direct",
]


def parse_plan(text: str) -> Decision:

    text = text.lower()

    if "both" in text:
        return "both"

    if "tool" in text:
        return "tool"

    if "retrieve" in text:
        return "retrieve"

    return "direct"
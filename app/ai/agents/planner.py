from typing import TypedDict


class RoutingDecision(TypedDict):
    decision: str
    selected_tool: str


def plan(question: str) -> RoutingDecision:

    q = question.lower()

    if any(
        keyword in q
        for keyword in [
            "joke",
            "funny",
        ]
    ):
        return {
            "decision": "tool",
            "selected_tool": "joke",
        }

    if any(
        keyword in q
        for keyword in [
            "latest alert",
            "last alert",
            "recent alert",
        ]
    ):
        return {
            "decision": "tool",
            "selected_tool": "latest_alert",
        }

    if any(
        keyword in q
        for keyword in [
            "alert statistics",
            "alert stats",
            "how many alerts",
        ]
    ):
        return {
            "decision": "tool",
            "selected_tool": "alert_stats",
        }

    if any(
        keyword in q
        for keyword in [
            "how many satellites",
            "satellite count",
            "number of satellites",
        ]
    ):
        return {
            "decision": "tool",
            "selected_tool": "satellite_count",
        }

    if any(
        keyword in q
        for keyword in [
            "list satellites",
            "show satellites",
            "registered satellites",
        ]
    ):
        return {
            "decision": "tool",
            "selected_tool": "satellite_list",
        }

    if any(
        keyword in q
        for keyword in [
            "battery",
            "telemetry",
            "temperature",
            "communication",
            "signal",
            "orbit",
            "velocity",
            "altitude",
            "satellite",
            "anomaly",
            "mission",
            "ground station",
        ]
    ):
        return {
            "decision": "retrieve",
            "selected_tool": "",
        }

    return {
        "decision": "direct",
        "selected_tool": "",
    }
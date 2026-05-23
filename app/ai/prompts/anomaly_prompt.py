from typing import List


def build_anomaly_prompt(
    satellite_name: str,
    alert_message: str,
    telemetry_points: List[dict],
) -> str:

    telemetry_summary = "\n".join([
        f"{point['parameter']}: {point['value']}"
        for point in telemetry_points
    ])

    return f"""
Satellite: {satellite_name}

Alert:
{alert_message}

Telemetry:
{telemetry_summary}

Analyze:
1. Operational summary
2. Most likely cause
3. Recommended action
4. Severity
"""
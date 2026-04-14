from app.telemetry.api.schemas import TelemetryCreate, TelemetryEventCreate


def legacy_to_event(legacy: TelemetryCreate) -> TelemetryEventCreate:

    return TelemetryEventCreate(
        satellite_id=legacy.satellite_id,
        timestamp=legacy.timestamp,
        parameters=[
            {"name": "temperature", "value": legacy.temperature},
            {"name": "velocity", "value": legacy.velocity},
            {"name": "altitude", "value": legacy.altitude},
        ],
    )
from fastapi import APIRouter
import json

from app.core.redis import redis_client

from app.telemetry.api.schemas import (
    TelemetryBatchCreate,
    TelemetryEventBatchCreate,
)
from app.telemetry.services.adapters import legacy_to_event

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

STREAM_NAME = "telemetry_stream"


@router.post("/events/batch")
def ingest_events(
    payload: TelemetryEventBatchCreate,
):
    """
    New ingestion endpoint (parameter-based).
    Sends events to Redis Stream instead of processing synchronously.
    """

    events_data = [event.model_dump() for event in payload.events]

    redis_client.xadd(
        STREAM_NAME,
        {"data": json.dumps(events_data)},
    )

    return {
        "status": "queued",
        "events_received": len(events_data),
    }


@router.post("/batch")
def ingest_legacy(
    payload: TelemetryBatchCreate,
):
    """
    Legacy ingestion endpoint.
    Converts old format → new event format → enqueues.
    """

    events = [legacy_to_event(m) for m in payload.measurements]
    events_data = [event.model_dump() for event in events]

    redis_client.xadd(
        STREAM_NAME,
        {"data": json.dumps(events_data)},
    )

    return {
        "status": "queued",
        "events_received": len(events_data),
    }
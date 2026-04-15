from fastapi import APIRouter
import json
import uuid

from app.core.redis import redis_client
from app.telemetry.api.schemas import TelemetryEventBatchCreate

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

STREAM_NAME = "telemetry_stream"


@router.post("/events/batch")
def ingest_events(payload: TelemetryEventBatchCreate):
    try:
        # ✅ Use Pydantic JSON-safe serialization
        events_data = []

        for event in payload.events:
            event_dict = event.model_dump(mode="json")

            # ✅ Inject event_id (not part of schema)
            event_dict["event_id"] = str(uuid.uuid4())

            events_data.append(event_dict)

        # Optional debug (remove later)
        print("EVENTS DATA:", events_data)

        redis_client.xadd(
            STREAM_NAME,
            {
                "data": json.dumps(events_data),
                "retry_count": "0",  # Redis stores strings
            }
        )

        return {
            "status": "queued",
            "events_received": len(events_data),
        }

    except Exception as e:
        print("ERROR in ingest_events:", e)
        raise
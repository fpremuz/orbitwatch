from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import logger
from app.core.redis import redis_client

from app.telemetry.api.schemas import (
    TelemetryEventBatchCreate,
)

from app.telemetry.domain.point_models import (
    TelemetryPoint,
)

from app.telemetry.domain.parameter_models import (
    TelemetryParameter,
)

import json
import uuid


router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry"],
)

STREAM_NAME = "telemetry_stream"


@router.post("/events/batch")
def ingest_events(payload: TelemetryEventBatchCreate):

    try:

        events_data = []

        for event in payload.events:

            event_dict = event.model_dump(
                mode="json"
            )

            event_dict["event_id"] = str(
                uuid.uuid4()
            )

            events_data.append(event_dict)

        logger.info(
            "Telemetry batch received",
            extra={
                "events_received": len(events_data),
            }
        )

        redis_client.xadd(
            STREAM_NAME,
            {
                "data": json.dumps(events_data),
                "retry_count": "0",
            }
        )

        return {
            "status": "queued",
            "events_received": len(events_data),
        }

    except Exception as e:

        logger.exception(
            "Telemetry ingestion failed"
        )

        raise e


@router.get("/history/{satellite_id}")
def get_telemetry_history(
    satellite_id: str,
    parameter: str = Query(...),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
):

    query = (
        db.query(
            TelemetryPoint.timestamp,
            TelemetryPoint.value,
        )
        .join(
            TelemetryParameter,
            TelemetryPoint.parameter_id
            == TelemetryParameter.id,
        )
        .filter(
            TelemetryPoint.satellite_id
            == satellite_id
        )
        .filter(
            TelemetryParameter.name
            == parameter
        )
        .order_by(  
            TelemetryPoint.timestamp.desc()
        )
        .limit(limit)
    )

    results = query.all()

    return [
        {
            "timestamp": row.timestamp,
            "value": row.value,
        }
        for row in reversed(results)
    ]
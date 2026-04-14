from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db

from app.telemetry.api.schemas import (
    TelemetryBatchCreate,
    TelemetryEventBatchCreate,
    TelemetryResponse
)

from app.telemetry.services.ingestion_service import TelemetryIngestionService
from app.telemetry.services.query_service import TelemetryQueryService


router = APIRouter(prefix="/telemetry", tags=["Telemetry"])


# ----------------------------
# Batch ingestion endpoint
# ----------------------------

@router.post("/batch")
def ingest_batch(
    payload: TelemetryBatchCreate,
    db: Session = Depends(get_db),
):

    service = TelemetryIngestionService(db)
    return service.ingest_batch(payload.measurements)


# ----------------------------
# Query telemetry
# ----------------------------

@router.get("", response_model=List[TelemetryResponse])
def get_telemetry(
    satellite_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    cursor: Optional[datetime] = None,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
):

    service = TelemetryQueryService(db)

    return service.get_telemetry(
        satellite_id=satellite_id,
        start_time=start_time,
        end_time=end_time,
        cursor=cursor,
        limit=limit,
    )

@router.post("/events/batch")
def ingest_events(
    payload: TelemetryEventBatchCreate,
    db: Session = Depends(get_db),
):
    service = TelemetryIngestionService(db)
    return service.ingest_event_batch(payload.events)
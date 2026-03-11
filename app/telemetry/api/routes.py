from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.telemetry.api.schemas import TelemetryCreate, TelemetryResponse
from app.telemetry.api.schemas import TelemetryBatchCreate
from app.telemetry.services.ingestion_service import TelemetryIngestionService

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

@router.post("/batch")
def ingest_batch(
    payload: TelemetryBatchCreate,
    db: Session = Depends(get_db),
):
    service = TelemetryIngestionService(db)
    return service.ingest_batch(payload.measurements)
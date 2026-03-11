from sqlalchemy.orm import Session
from app.telemetry.infrastructure.repository import TelemetryRepository


class TelemetryIngestionService:

    def __init__(self, db: Session):
        self.repo = TelemetryRepository(db)

    def ingest(self, payload):
        return self.repo.create(
            satellite_id=payload.satellite_id,
            temperature=payload.temperature,
            velocity=payload.velocity,
            altitude=payload.altitude,
        )
    
    def ingest_batch(self, measurements):
        return self.repo.create_batch(measurements) 
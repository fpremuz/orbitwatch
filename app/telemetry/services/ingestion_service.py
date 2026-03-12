from sqlalchemy.orm import Session
from app.telemetry.infrastructure.repository import TelemetryRepository
from app.telemetry.domain.models import Telemetry


class TelemetryIngestionService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = TelemetryRepository(db)

    def ingest_batch(self, measurements):

        telemetry_objects = [
            Telemetry(
                satellite_id=m.satellite_id,
                timestamp=m.timestamp,
                temperature=m.temperature,
                velocity=m.velocity,
                altitude=m.altitude,
            )
            for m in measurements
        ]

        self.repo.create_batch(telemetry_objects)

        self.db.commit()

        return telemetry_objects
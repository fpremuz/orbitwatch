from pytest import Session

from app.telemetry.domain.models import Telemetry
from app.telemetry.services.processor import TelemetryProcessor


class TelemetryIngestionService:

    def __init__(self, db: Session):

        self.db = db
        self.processor = TelemetryProcessor(db)

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

        alerts = self.processor.process_batch(telemetry_objects)

        self.db.commit()

        return {
            "processed": len(telemetry_objects),
            "alerts_generated": len(alerts),
        }
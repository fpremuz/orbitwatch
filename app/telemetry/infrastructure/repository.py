from sqlalchemy.orm import Session
from app.telemetry.domain.models import Telemetry


class TelemetryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, satellite_id, temperature, velocity, altitude):
        telemetry = Telemetry(
            satellite_id=satellite_id,
            temperature=temperature,
            velocity=velocity,
            altitude=altitude,
        )

        self.db.add(telemetry)
        self.db.commit()
        self.db.refresh(telemetry)

        return telemetry

    def create_batch(self, measurements):
        telemetry_objects = [
            Telemetry(
                satellite_id=m.satellite_id,
                temperature=m.temperature,
                velocity=m.velocity,
                altitude=m.altitude,
            )
            for m in measurements
        ]

        self.db.add_all(telemetry_objects)
        self.db.commit()

        return telemetry_objects

    def get_by_satellite(self, satellite_id):
        return (
            self.db.query(Telemetry)
            .filter(Telemetry.satellite_id == satellite_id)
            .order_by(Telemetry.timestamp.desc())
            .all()
        )
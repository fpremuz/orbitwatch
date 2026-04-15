from sqlalchemy.orm import Session
from app.telemetry.domain.models import Telemetry
from sqlalchemy.exc import IntegrityError


class TelemetryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, telemetry: Telemetry):
        self.db.add(telemetry)
        return telemetry

    def create_batch(self, telemetry_points):
        try:
            self.db.add_all(telemetry_points)
            self.db.flush()
        except IntegrityError:
            self.db.rollback()

    def get_window(
        self,
        satellite_id,
        start_time=None,
        end_time=None,
        cursor=None,
        limit=100,
    ):
        query = self.db.query(Telemetry).filter(
            Telemetry.satellite_id == satellite_id
        )

        if start_time:
            query = query.filter(Telemetry.timestamp >= start_time)

        if end_time:
            query = query.filter(Telemetry.timestamp <= end_time)

        if cursor:
            query = query.filter(Telemetry.timestamp < cursor)

        return (
            query.order_by(Telemetry.timestamp.desc())
            .limit(limit)
            .all()
        )
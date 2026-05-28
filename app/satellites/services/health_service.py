from datetime import datetime, UTC, timedelta

from sqlalchemy.orm import Session

from app.alerts.domain.models import Alert
from app.satellites.domain.models import Satellite


class SatelliteHealthService:

    def __init__(self, db: Session):

        self.db = db

    def recalculate_health(self, satellite):

        score = 100.0

        window_start = datetime.now(UTC) - timedelta(minutes=10)

        alerts = (
            self.db.query(Alert)
            .filter(
                Alert.satellite_id == satellite.id,
                Alert.status == "ACTIVE",
                Alert.created_at >= window_start,
            )
            .all()
        )

        for alert in alerts:

            severity = alert.severity

            if severity == "WARNING":
                score -= 2

            elif severity == "CRITICAL":
                score -= 10

            elif severity == "ANOMALY":
                score -= 5

        if satellite.last_seen_at:

            now = datetime.now(UTC)

            seconds_since_seen = (
                now - satellite.last_seen_at
            ).total_seconds()

            if seconds_since_seen > 60:
                score -= 20

        score = max(0, min(100, score))

        satellite.health_score = round(score, 2)

        return satellite.health_score
from sqlalchemy.orm import Session

from app.telemetry.domain.models import Telemetry
from app.telemetry.services.limit_engine import LimitEngine
from app.alerts.infrastructure.repository import AlertRepository


class TelemetryProcessor:

    def __init__(self, db: Session):
        self.db = db
        self.alert_repo = AlertRepository(db)
        self.limit_engine = LimitEngine()

    def process_batch(self, telemetry_objects: list[Telemetry]):

        alerts = []

        for telemetry in telemetry_objects:

            # Store telemetry
            self.repo.create(telemetry)

            # Evaluate limits
            generated_alerts = self.limit_engine.evaluate(telemetry)

            for alert in generated_alerts:
                self.alert_repo.create(alert)

            alerts.extend(generated_alerts)

        return alerts
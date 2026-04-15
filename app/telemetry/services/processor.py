from app.telemetry.infrastructure.repository import TelemetryRepository
from app.telemetry.services.limit_engine import TelemetryLimitEngine
from app.alerts.infrastructure.repository import AlertRepository


class TelemetryProcessor:

    def __init__(self, db):
        self.db = db
        self.repo = TelemetryRepository(db)
        self.limit_engine = TelemetryLimitEngine(db)
        self.alert_repo = AlertRepository(db)

    def process_batch(self, telemetry_points):

        alerts = []

        # 1️⃣ Persist telemetry in bulk
        self.repo.create_batch(telemetry_points)

        # 2️⃣ Evaluate limits
        for point in telemetry_points:

            generated_alerts = self.limit_engine.evaluate_point(point)

            for alert in generated_alerts:
                self.alert_repo.create(alert)

            alerts.extend(
                self.limit_engine.evaluate_point(point)
            )

        return alerts
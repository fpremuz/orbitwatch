from app.alerts.domain.models import Alert
from app.telemetry.domain.parameter_models import TelemetryParameter


class TelemetryLimitEngine:

    def __init__(self, db):
        self.db = db

    def evaluate_point(self, point):
        alerts = []

        # 🔥 Resolve parameter from DB (source of truth)
        parameter = self.db.get(TelemetryParameter, point.parameter_id)

        if not parameter:
            # Defensive programming (don't silently fail)
            raise Exception(f"Parameter {point.parameter_id} not found")

        parameter_name = parameter.name

        # 🔥 Example rule
        if point.value > 95:
            alerts.append(
                Alert(
                    satellite_id=point.satellite_id,
                    parameter=parameter_name,
                    level="CRITICAL",
                    message=f"{parameter_name} exceeded threshold",
                )
            )

        return alerts
from app.alerts.domain.models import Alert


class TelemetryLimitEngine:
    """
    Responsible for evaluating telemetry points against limits
    and generating alerts.
    """

    def evaluate_point(self, point):

        alerts = []

        # TEMP: hardcoded rule (will be replaced later)
        if point.value > 95:
            alerts.append(
                Alert(
                    satellite_id=point.satellite_id,
                    parameter_id=point.parameter_id,
                    level="CRITICAL",
                    message="Value exceeded critical threshold",
                )
            )

        return alerts
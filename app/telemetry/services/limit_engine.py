from app.telemetry.domain.models import Telemetry
from app.alerts.domain.models import Alert


class LimitEngine:

    def evaluate(self, telemetry: Telemetry):

        alerts = []

        # Temperature limits
        if telemetry.temperature > 95:
            alerts.append(
                Alert(
                    satellite_id=telemetry.satellite_id,
                    parameter="temperature",
                    level="CRITICAL",
                    message="Temperature exceeded critical threshold",
                )
            )

        elif telemetry.temperature > 80:
            alerts.append(
                Alert(
                    satellite_id=telemetry.satellite_id,
                    parameter="temperature",
                    level="WARNING",
                    message="Temperature exceeded warning threshold",
                )
            )

        return alerts
from app.alerts.domain.models import Alert


def evaluate_point(self, point):

    alerts = []

    # TEMP: still hardcoded
    if point.value > 95:
        alerts.append(
            Alert(
                satellite_id=point.satellite_id,
                parameter="unknown",  # fix later
                level="CRITICAL",
                message="Value exceeded critical threshold",
            )
        )

    return alerts
from statistics import mean, stdev

from sqlalchemy import select

from app.alerts.domain.models import Alert
from app.telemetry.domain.point_models import TelemetryPoint


class AnomalyDetector:

    def __init__(self, db):
        self.db = db

    def evaluate_point(self, point, parameter_name: str):

        alerts = []

        stmt = (
            select(TelemetryPoint)
            .where(
                TelemetryPoint.satellite_id == point.satellite_id,
                TelemetryPoint.parameter_id == point.parameter_id,
            )
            .order_by(TelemetryPoint.timestamp.desc())
            .limit(20)
        )

        recent_points = self.db.execute(stmt).scalars().all()

        values = [p.value for p in recent_points]

        # Need enough history
        if len(values) < 5:
            return alerts

        avg = mean(values)

        try:
            std_dev = stdev(values)
        except Exception:
            return alerts

        # Avoid divide-by-zero
        if std_dev == 0:
            return alerts

        z_score = abs(point.value - avg) / std_dev

        # Threshold
        if z_score > 3:

            alerts.append(
                Alert(
                    satellite_id=point.satellite_id,
                    parameter=parameter_name,
                    level="ANOMALY",
                    message=(
                        f"Anomaly detected for {parameter_name}. "
                        f"Value={point.value:.2f}, "
                        f"mean={avg:.2f}, "
                        f"z-score={z_score:.2f}"
                    )
                )
            )

        return alerts
from collections import defaultdict
from statistics import mean, pstdev

from app.core.logging import logger
from app.alerts.domain.models import Alert
from app.telemetry.domain.point_models import TelemetryPoint


class TelemetryLimitEngine:

    def __init__(self, db):
        self.db = db

    def evaluate_point(self, point, parameter_name):

        alerts = []

        LIMITS = {
            "temperature_c": 70,
            "battery_voltage": 4.0,
            "altitude_km": 1000,
            "velocity_kmh": 28500,
        }

        threshold = LIMITS.get(parameter_name)

        if threshold and point.value > threshold:

            logger.warning(
                "Threshold exceeded",
                extra={
                    "parameter": parameter_name,
                    "value": point.value,
                    "threshold": threshold,
                }
            )

            alerts.append(
                Alert(
                    satellite_id=point.satellite_id,
                    parameter=parameter_name,
                    severity="CRITICAL",
                    message=(
                        f"{parameter_name} exceeded threshold "
                        f"({point.value} > {threshold})"
                    ),
                )
            )

        # Anomaly detection
        anomaly_alert = self.detect_anomaly(
            point,
            parameter_name,
        )

        if anomaly_alert:
            alerts.append(anomaly_alert)

        # Persist alerts
        for alert in alerts:
            self.db.add(alert)

        return alerts

    def detect_anomaly(self, point, parameter_name):

        historical_points = (
            self.db.query(TelemetryPoint)
            .filter(
                TelemetryPoint.satellite_id == point.satellite_id,
                TelemetryPoint.parameter_id == point.parameter_id,
            )
            .order_by(TelemetryPoint.timestamp.desc())
            .limit(20)
            .all()
        )

        values = [p.value for p in historical_points]

        if len(values) < 5:
            return None

        avg = mean(values)
        std_dev = pstdev(values)

        if std_dev == 0:
            return None

        z_score = abs(point.value - avg) / std_dev

        logger.info(
            "Anomaly evaluation",
            extra={
                "parameter": parameter_name,
                "value": point.value,
                "average": avg,
                "std_dev": std_dev,
                "z_score": z_score,
            }
        )

        if z_score > 3:

            logger.warning("🚨 ANOMALY DETECTED")

            return Alert(
                satellite_id=point.satellite_id,
                parameter=parameter_name,
                severity="ANOMALY",
                message=(
                    f"Anomalous {parameter_name} value detected: "
                    f"{point.value}"
                ),
            )

        return None
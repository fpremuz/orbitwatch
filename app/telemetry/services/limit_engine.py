from collections import defaultdict
from statistics import mean, pstdev
from datetime import datetime, UTC, timedelta

from app.core.logging import logger
from app.alerts.domain.models import Alert
from app.telemetry.domain.point_models import TelemetryPoint


class TelemetryLimitEngine:

    # -----------------------------------
    # Parameter-specific thresholds
    # -----------------------------------
    LIMITS = {
        "temperature_c": 75,
        "battery_voltage": 4.1,
        "altitude_km": 1500,
        "velocity_kmh": 30000,
    }

    # Prevent duplicate alerts
    ALERT_COOLDOWN_MINUTES = 5

    def __init__(self, db):

        self.db = db

    def evaluate_point(self, point, parameter_name):

        alerts = []

        # -----------------------------------
        # Static threshold alert
        # -----------------------------------
        limit = self.LIMITS.get(parameter_name)

        if limit and point.value > limit:

            existing_critical = (
                self.db.query(Alert)
                .filter(
                    Alert.satellite_id == point.satellite_id,
                    Alert.parameter == parameter_name,
                    Alert.severity == "CRITICAL",
                    Alert.created_at >= (
                        datetime.now(UTC)
                        - timedelta(
                            minutes=self.ALERT_COOLDOWN_MINUTES
                        )
                    ),
                )
                .first()
            )

            if not existing_critical:

                alerts.append(
                    Alert(
                        satellite_id=point.satellite_id,
                        parameter=parameter_name,
                        severity="CRITICAL",
                        message=(
                            f"{parameter_name} exceeded threshold "
                            f"({point.value} > {limit})"
                        ),
                    )
                )

        # -----------------------------------
        # Anomaly detection
        # -----------------------------------
        anomaly_alert = self.detect_anomaly(
            point,
            parameter_name,
        )

        if anomaly_alert:
            alerts.append(anomaly_alert)

        # -----------------------------------
        # Persist alerts
        # -----------------------------------
        for alert in alerts:

            self.db.add(alert)

        return alerts

    def detect_anomaly(
        self,
        point,
        parameter_name,
    ):

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

            existing_anomaly = (
                self.db.query(Alert)
                .filter(
                    Alert.satellite_id == point.satellite_id,
                    Alert.parameter == parameter_name,
                    Alert.severity == "ANOMALY",
                    Alert.created_at >= (
                        datetime.now(UTC)
                        - timedelta(
                            minutes=self.ALERT_COOLDOWN_MINUTES
                        )
                    ),
                )
                .first()
            )

            if existing_anomaly:
                return None

            logger.warning(
                "🚨 ANOMALY DETECTED",
                extra={
                    "parameter": parameter_name,
                    "value": point.value,
                    "z_score": z_score,
                }
            )

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
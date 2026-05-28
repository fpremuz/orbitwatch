from statistics import mean, pstdev
from datetime import datetime, UTC, timedelta

from app.core.logging import logger
from app.alerts.domain.models import Alert
from app.telemetry.domain.point_models import TelemetryPoint


class TelemetryLimitEngine:

    LIMITS = {
        "temperature_c": 75,
        "battery_voltage": 4.1,
        "altitude_km": 1500,
        "velocity_kmh": 30000,
    }

    ALERT_COOLDOWN_MINUTES = 5

    def __init__(self, db):

        self.db = db

    def evaluate_point(
        self,
        point,
        parameter_name,
    ):

        alerts = []

        limit = self.LIMITS.get(parameter_name)

        # -----------------------------------
        # CRITICAL ALERT LOGIC
        # -----------------------------------
        active_critical = (
            self.db.query(Alert)
            .filter(
                Alert.satellite_id == point.satellite_id,
                Alert.parameter == parameter_name,
                Alert.severity == "CRITICAL",
                Alert.status == "ACTIVE",
            )
            .first()
        )

        exceeds_limit = (
            limit is not None
            and point.value > limit
        )

        # Create alert
        if exceeds_limit and not active_critical:

            alert = Alert(
                satellite_id=point.satellite_id,
                parameter=parameter_name,
                severity="CRITICAL",
                status="ACTIVE",
                message=(
                    f"{parameter_name} exceeded threshold "
                    f"({point.value} > {limit})"
                ),
            )

            alerts.append(alert)

        # Resolve alert
        elif not exceeds_limit and active_critical:

            active_critical.status = "RESOLVED"
            active_critical.resolved_at = datetime.now(UTC)

            logger.info(
                "Critical alert resolved",
                extra={
                    "satellite_id": str(point.satellite_id),
                    "parameter": parameter_name,
                }
            )

        # -----------------------------------
        # ANOMALY DETECTION
        # -----------------------------------
        anomaly_alert = self.detect_anomaly(
            point,
            parameter_name,
        )

        if anomaly_alert:
            alerts.append(anomaly_alert)

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

        active_anomaly = (
            self.db.query(Alert)
            .filter(
                Alert.satellite_id == point.satellite_id,
                Alert.parameter == parameter_name,
                Alert.severity == "ANOMALY",
                Alert.status == "ACTIVE",
            )
            .first()
        )

        # Create anomaly
        if z_score > 3:

            if active_anomaly:
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
                status="ACTIVE",
                message=(
                    f"Anomalous {parameter_name} value detected: "
                    f"{point.value}"
                ),
            )

        # Resolve anomaly
        else:

            if active_anomaly:

                active_anomaly.status = "RESOLVED"
                active_anomaly.resolved_at = datetime.now(UTC)

                logger.info(
                    "Anomaly resolved",
                    extra={
                        "satellite_id": str(point.satellite_id),
                        "parameter": parameter_name,
                    }
                )

        return None
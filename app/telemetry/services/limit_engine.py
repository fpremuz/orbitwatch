from statistics import mean, pstdev
from datetime import datetime, UTC

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

    def __init__(self, db):

        self.db = db

    def evaluate_point(
        self,
        point,
        parameter_name,
    ):

        alerts = []

        limit = self.LIMITS.get(
            parameter_name
        )

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

        # -----------------------------------
        # CRITICAL ALERT CREATION
        # -----------------------------------

        if (
            limit is not None
            and point.value > limit
        ):

            if not active_critical:

                critical_alert = Alert(
                    satellite_id=point.satellite_id,
                    parameter=parameter_name,
                    severity="CRITICAL",
                    status="ACTIVE",
                    message=(
                        f"{parameter_name} exceeded "
                        f"threshold ({point.value})"
                    ),
                )

                alerts.append(
                    critical_alert
                )

                logger.warning(
                    "CRITICAL ALERT CREATED",
                    extra={
                        "parameter": parameter_name,
                        "value": point.value,
                    }
                )

        # -----------------------------------
        # CRITICAL ALERT RESOLUTION
        # -----------------------------------

        else:

            if active_critical:

                active_critical.status = (
                    "RESOLVED"
                )

                active_critical.resolved_at = (
                    datetime.now(UTC)
                )

                logger.info(
                    "CRITICAL ALERT RESOLVED",
                    extra={
                        "parameter": parameter_name,
                    }
                )

        # -----------------------------------
        # ANOMALY DETECTION
        # -----------------------------------

        anomaly_alert = (
            self.detect_anomaly(
                point,
                parameter_name,
            )
        )

        if anomaly_alert:

            alerts.append(
                anomaly_alert
            )

        # -----------------------------------
        # Persist alerts
        # -----------------------------------

        for alert in alerts:

            self.db.add(alert)

            import json

            from app.core.redis import (
                redis_client,
            )

            redis_client.publish(
                "telemetry_events",

                json.dumps({

                    "type": "alert_created",

                    "alert": {

                        "satellite_id": str(
                            alert.satellite_id
                        ),

                        "parameter": (
                            alert.parameter
                        ),

                        "severity": (
                            alert.severity
                        ),

                        "message": (
                            alert.message
                        ),
                    },
                })
            )

        return alerts

    def detect_anomaly(
        self,
        point,
        parameter_name,
    ):

        historical_points = (
            self.db.query(
                TelemetryPoint
            )
            .filter(
                TelemetryPoint.satellite_id
                == point.satellite_id,

                TelemetryPoint.parameter_id
                == point.parameter_id,
            )
            .order_by(
                TelemetryPoint.timestamp.desc()
            )
            .limit(20)
            .all()
        )

        values = [
            p.value
            for p in historical_points
        ]

        if len(values) < 5:
            return None

        avg = mean(values)

        std_dev = pstdev(values)

        if std_dev == 0:
            return None

        z_score = (
            abs(point.value - avg)
            / std_dev
        )

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
                Alert.satellite_id
                == point.satellite_id,

                Alert.parameter
                == parameter_name,

                Alert.severity
                == "ANOMALY",

                Alert.status
                == "ACTIVE",
            )
            .first()
        )

        # -----------------------------------
        # CREATE ANOMALY
        # -----------------------------------

        if z_score > 3:

            if active_anomaly:
                return None

            logger.warning(
                "ANOMALY DETECTED",
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
                    f"Anomalous "
                    f"{parameter_name} value "
                    f"detected: {point.value}"
                ),
            )

        # -----------------------------------
        # RESOLVE ANOMALY
        # -----------------------------------

        else:

            if active_anomaly:

                active_anomaly.status = (
                    "RESOLVED"
                )

                active_anomaly.resolved_at = (
                    datetime.now(UTC)
                )

                logger.info(
                    "ANOMALY RESOLVED",
                    extra={
                        "satellite_id": str(
                            point.satellite_id
                        ),
                        "parameter": parameter_name,
                    }
                )

        return None
from sqlalchemy.orm import Session

from app.alerts.domain.models import Alert
from app.telemetry.domain.point_models import TelemetryPoint


class DetectionService:

    BATTERY_CRITICAL_THRESHOLD = 20
    TEMPERATURE_CRITICAL_THRESHOLD = 85

    @staticmethod
    def analyze(db: Session, telemetry_point: TelemetryPoint):

        alerts_created = []

        parameter_name = telemetry_point.parameter.name.lower()
        value = telemetry_point.value

        # Battery anomaly
        if parameter_name == "battery_voltage":

            if value < DetectionService.BATTERY_CRITICAL_THRESHOLD:

                alert = Alert(
                    satellite_id=telemetry_point.satellite_id,
                    severity="critical",
                    message=f"Battery voltage critically low: {value}V"
                )

                db.add(alert)
                alerts_created.append(alert)

        # Temperature anomaly
        if parameter_name == "temperature":

            if value > DetectionService.TEMPERATURE_CRITICAL_THRESHOLD:

                alert = Alert(
                    satellite_id=telemetry_point.satellite_id,
                    severity="critical",
                    message=f"Temperature critically high: {value}°C"
                )

                db.add(alert)
                alerts_created.append(alert)

        if alerts_created:
            db.commit()

            for alert in alerts_created:
                db.refresh(alert)

        return alerts_created
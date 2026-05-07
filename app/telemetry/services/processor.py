from app.telemetry.services.limit_engine import TelemetryLimitEngine


class TelemetryProcessor:

    def __init__(self, db):
        self.limit_engine = TelemetryLimitEngine(db)

    def process_batch(self, telemetry_points):

        alerts = []

        for item in telemetry_points:

            point = item["point"]
            parameter_name = item["parameter_name"]

            point_alerts = self.limit_engine.evaluate_point(
                point,
                parameter_name,
            )

            alerts.extend(point_alerts)

        return alerts
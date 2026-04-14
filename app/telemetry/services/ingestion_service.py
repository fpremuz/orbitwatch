from app.telemetry.services.parameter_service import ParameterService
from app.telemetry.domain.point_models import TelemetryPoint
from app.telemetry.services.processor import TelemetryProcessor


class TelemetryIngestionService:

    def __init__(self, db):
        self.db = db
        self.parameter_service = ParameterService(db)
        self.processor = TelemetryProcessor(db)

    def ingest_event_batch(self, events):

        telemetry_points = []

        for event in events:

            for param in event.parameters:

                parameter = self.parameter_service.get_or_create_parameter(
                    event.satellite_id,
                    param.name,
                )

                telemetry_points.append(
                    TelemetryPoint(
                        satellite_id=event.satellite_id,
                        parameter_id=parameter.id,
                        timestamp=event.timestamp,
                        value=param.value,
                    )
                )

        alerts = self.processor.process_batch(telemetry_points)

        self.db.commit()

        return {
            "processed": len(telemetry_points),
            "alerts_generated": len(alerts),
        }
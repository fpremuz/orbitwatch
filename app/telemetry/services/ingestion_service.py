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

        # 1️⃣ Group events by satellite (important)
        events_by_satellite = {}

        for event in events:
            events_by_satellite.setdefault(event.satellite_id, []).append(event)

        for satellite_id, sat_events in events_by_satellite.items():

            # 2️⃣ Collect all parameter names
            parameter_names = set()

            for event in sat_events:
                for param in event.parameters:
                    parameter_names.add(param.name)

            # 3️⃣ Resolve parameters in bulk
            parameter_map = self.parameter_service.get_or_create_parameters_bulk(
                satellite_id,
                parameter_names,
            )

            # 4️⃣ Create telemetry points
            for event in sat_events:
                for param in event.parameters:

                    parameter = parameter_map[param.name]

                    telemetry_points.append(
                        TelemetryPoint(
                            satellite_id=satellite_id,
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
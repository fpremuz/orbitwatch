from collections import defaultdict

from app.telemetry.services.parameter_service import ParameterService
from app.telemetry.domain.point_models import TelemetryPoint
from app.telemetry.services.processor import TelemetryProcessor


class TelemetryIngestionService:

    def __init__(self, db):
        self.db = db
        self.parameter_service = ParameterService(db)
        self.processor = TelemetryProcessor(db)

    def ingest_event_batch(self, events):
        """
        events: list[dict]
        Each event:
        {
            "event_id": str,
            "satellite_id": str,
            "timestamp": str/datetime,
            "parameters": [
                {"name": str, "value": float}
            ]
        }
        """

        telemetry_points = []

        # 1️⃣ Group events by satellite
        events_by_satellite = defaultdict(list)

        for event in events:
            satellite_id = event["satellite_id"]
            events_by_satellite[satellite_id].append(event)

        # 2️⃣ Process per satellite (important for bulk resolution)
        for satellite_id, sat_events in events_by_satellite.items():

            # Collect all parameter names
            parameter_names = set()

            for event in sat_events:
                for param in event["parameters"]:
                    parameter_names.add(param["name"])

            # Resolve parameters in bulk
            parameter_map = self.parameter_service.get_or_create_parameters_bulk(
                satellite_id,
                parameter_names,
            )

            # Build telemetry points
            for event in sat_events:

                event_id = event["event_id"]
                timestamp = event["timestamp"]

                for param in event["parameters"]:

                    parameter = parameter_map[param["name"]]

                    telemetry_points.append(
                        TelemetryPoint(
                            event_id=event_id,
                            satellite_id=satellite_id,
                            parameter_id=parameter.id,
                            timestamp=timestamp,
                            value=param["value"],
                        )
                    )

        # 3️⃣ Process + persist
        alerts = self.processor.process_batch(telemetry_points)

        # 4️⃣ Commit transaction
        self.db.commit()

        return {
            "processed": len(telemetry_points),
            "alerts_generated": len(alerts),
        }
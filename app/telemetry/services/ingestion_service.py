from collections import defaultdict
from datetime import datetime

from app.telemetry.services.parameter_service import ParameterService
from app.telemetry.domain.point_models import TelemetryPoint
from app.telemetry.services.processor import TelemetryProcessor
from app.satellites.domain.models import Satellite


class TelemetryIngestionService:

    def __init__(self, db):
        self.db = db
        self.parameter_service = ParameterService(db)
        self.processor = TelemetryProcessor(db)

    def ingest_event_batch(self, events):
        """
        events: list[dict]
        """

        telemetry_points = []

        # 1️⃣ Group events by satellite
        events_by_satellite = defaultdict(list)

        for event in events:
            satellite_id = event["satellite_id"]
            events_by_satellite[satellite_id].append(event)

        # 2️⃣ Process per satellite
        for satellite_id, sat_events in events_by_satellite.items():

            # ✅ Validate satellite exists EARLY
            satellite = self.db.get(Satellite, satellite_id)
            if not satellite:
                raise Exception(f"Satellite {satellite_id} not found")

            # 3️⃣ Collect parameter names
            parameter_names = set()
            for event in sat_events:
                for param in event["parameters"]:
                    parameter_names.add(param["name"])

            # 4️⃣ Resolve parameters in bulk
            parameter_map = self.parameter_service.get_or_create_parameters_bulk(
                satellite_id,
                parameter_names,
            )

            # 5️⃣ Build telemetry points
            for event in sat_events:

                event_id = event["event_id"]

                # ✅ Normalize timestamp
                timestamp = event["timestamp"]
                if isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(
                        timestamp.replace("Z", "+00:00")
                    )

                for param in event["parameters"]:

                    parameter = parameter_map[param["name"]]

                    telemetry_points.append(
                        TelemetryPoint(
                            event_id=event_id,
                            satellite_id=satellite_id,
                            parameter_id=parameter.id,
                            timestamp=timestamp,
                            value=param["value"],
                            parameter_name=parameter.name,
                        )
                    )

        # 6️⃣ Process + persist
        alerts = self.processor.process_batch(telemetry_points)

        for alert in alerts:
            print(f"🚨 ALERT: {alert.parameter} | {alert.level} | {alert.message}")

        # 7️⃣ Commit transaction
        self.db.commit()

        return {
            "processed": len(telemetry_points),
            "alerts_generated": len(alerts),
        }
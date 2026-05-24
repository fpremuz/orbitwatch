from collections import defaultdict

from sqlalchemy import select

from app.core.logging import logger

from app.satellites.domain.models import (
    Satellite,
)

from app.telemetry.domain.point_models import (
    TelemetryPoint,
)

from app.telemetry.services.parameter_service import (
    ParameterService,
)

from app.telemetry.services.processor import (
    TelemetryProcessor,
)


class TelemetryIngestionService:

    def __init__(self, db):

        self.db = db

        self.parameter_service = (
            ParameterService(db)
        )

        self.processor = (
            TelemetryProcessor(db)
        )

    def ingest_event_batch(
        self,
        events,
    ):

        telemetry_points = []

        # -----------------------------------
        # Group by satellite UUID
        # -----------------------------------
        events_by_satellite = defaultdict(
            list
        )

        for event in events:

            satellite_id = event[
                "satellite_id"
            ]

            events_by_satellite[
                satellite_id
            ].append(event)

        # -----------------------------------
        # Process per satellite
        # -----------------------------------
        for (
            satellite_id,
            sat_events,
        ) in events_by_satellite.items():

            satellite = (
                self.db.execute(
                    select(Satellite).where(
                        Satellite.id
                        == satellite_id
                    )
                )
                .scalar_one_or_none()
            )

            if not satellite:

                logger.warning(
                    "Satellite not found",
                    extra={
                        "satellite_id": (
                            str(satellite_id)
                        ),
                    }
                )

                continue

            parameter_names = set()

            # -----------------------------------
            # Collect parameter names
            # -----------------------------------
            for event in sat_events:

                for param in event[
                    "parameters"
                ]:

                    parameter_names.add(
                        param["name"]
                    )

            # -----------------------------------
            # Bulk resolve/create parameters
            # -----------------------------------
            parameter_map = (
                self.parameter_service
                .get_or_create_parameters_bulk(
                    satellite.id,
                    parameter_names,
                )
            )

            # -----------------------------------
            # Build telemetry points
            # -----------------------------------
            for event in sat_events:

                event_id = event[
                    "event_id"
                ]

                timestamp = event[
                    "timestamp"
                ]

                for param in event[
                    "parameters"
                ]:

                    parameter = (
                        parameter_map[
                            param["name"]
                        ]
                    )

                    point = (
                        TelemetryPoint(
                            event_id=event_id,

                            satellite_id=(
                                satellite.id
                            ),

                            parameter_id=(
                                parameter.id
                            ),

                            timestamp=(
                                timestamp
                            ),

                            value=param[
                                "value"
                            ],
                        )
                    )

                    self.db.add(
                        point
                    )

                    telemetry_points.append(
                        {
                            "point": point,

                            "parameter_name": (
                                parameter.name
                            ),
                        }
                    )

        # -----------------------------------
        # Process alerts/anomalies
        # -----------------------------------
        alerts = (
            self.processor.process_batch(
                telemetry_points
            )
        )

        # -----------------------------------
        # Commit transaction
        # -----------------------------------
        self.db.commit()

        return {

            "processed": len(
                telemetry_points
            ),

            "alerts_generated": len(
                alerts
            ),

            "alerts": [
                {
                    "id": str(alert.id),
                    "satellite_id": str(alert.satellite_id),
                    "message": alert.message,
                    "severity": alert.severity,
                    "created_at": alert.created_at.isoformat(),
                }
                for alert in alerts
            ]
        }
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db

from app.satellites.domain.models import (
    Satellite,
)

from app.telemetry.domain.point_models import (
    TelemetryPoint,
)

router = APIRouter(
    prefix="/satellites",
    tags=["Satellites"],
)


@router.get("/overview")
def get_satellites(
    db: Session = Depends(get_db),
):

    satellites = (
        db.query(Satellite)
        .all()
    )

    results = []

    now = datetime.utcnow()

    for satellite in satellites:

        latest_telemetry = (
            db.query(
                func.max(
                    TelemetryPoint.timestamp
                )
            )
            .filter(
                TelemetryPoint.satellite_id
                == satellite.id
            )
            .scalar()
        )

        status = "OFFLINE"

        if latest_telemetry:

            seconds_since_last_seen = (
                now - latest_telemetry
            ).total_seconds()

            if seconds_since_last_seen <= 10:
                status = "ONLINE"

            elif seconds_since_last_seen <= 30:
                status = "DELAYED"

        results.append(
            {
                "id": str(satellite.id),
                "name": satellite.name,
                "norad_id": satellite.norad_id,
                "orbit_type": satellite.orbit_type,
                "last_seen": latest_telemetry,
                "status": status,
            }
        )

    return results
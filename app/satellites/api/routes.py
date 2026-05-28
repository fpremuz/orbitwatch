from datetime import datetime, UTC

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

    now = datetime.now(UTC)

    for satellite in satellites:

        status = "OFFLINE"

        if satellite.last_seen_at:

            last_seen = (
                satellite.last_seen_at
            )

            if last_seen.tzinfo is None:

                last_seen = (
                    last_seen.replace(
                        tzinfo=UTC
                    )
                )

            seconds_since_last_seen = (
                now - last_seen
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
                "last_seen": (
                    satellite.last_seen_at
                ),
                "status": status,
                "health_score": (
                    satellite.health_score
                ),
            }
        )

    return results
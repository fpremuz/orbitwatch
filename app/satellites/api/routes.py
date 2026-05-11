from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db

from app.satellites.infrastructure.repository import (
    SatelliteRepository,
)

from app.satellites.api.schemas import (
    SatelliteCreate,
    SatelliteResponse,
)

from app.satellites.domain.models import Satellite
from app.alerts.domain.models import Alert

import uuid

router = APIRouter(
    prefix="/satellites",
    tags=["Satellites"],
)


@router.post(
    "/",
    response_model=SatelliteResponse
)
def create_satellite(
    payload: SatelliteCreate,
    db: Session = Depends(get_db),
):

    repo = SatelliteRepository(db)

    satellite = repo.create(
        name=payload.name,
        norad_id=payload.norad_id
    )

    return satellite


@router.get(
    "/",
    response_model=list[SatelliteResponse]
)
def list_satellites(
    db: Session = Depends(get_db),
):

    repo = SatelliteRepository(db)

    return repo.get_all()


@router.get(
    "/overview"
)
def satellite_overview(
    db: Session = Depends(get_db),
):

    satellites = (
        db.query(Satellite)
        .all()
    )

    result = []

    for satellite in satellites:

        alert_count = (
            db.query(func.count(Alert.id))
            .filter(
                Alert.satellite_id == satellite.id
            )
            .scalar()
        )

        latest_alert = (
            db.query(Alert)
            .filter(
                Alert.satellite_id == satellite.id
            )
            .order_by(Alert.created_at.desc())
            .first()
        )

        result.append({
            "id": str(satellite.id),
            "name": satellite.name,
            "norad_id": satellite.norad_id,
            "alert_count": alert_count,
            "latest_alert_level": (
                latest_alert.level
                if latest_alert
                else None
            ),
        })

    return result


@router.get(
    "/{satellite_id}",
    response_model=SatelliteResponse
)
def get_satellite(
    satellite_id: uuid.UUID,
    db: Session = Depends(get_db),
):

    repo = SatelliteRepository(db)

    satellite = repo.get_by_id(
        satellite_id
    )

    if not satellite:

        raise HTTPException(
            status_code=404,
            detail="Satellite not found"
        )

    return satellite
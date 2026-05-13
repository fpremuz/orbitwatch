from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.satellites.domain.models import Satellite

from app.api.schemas.satellites import (
    SatelliteResponse,
)


router = APIRouter(
    prefix="/satellites",
    tags=["Satellites"],
)


@router.get(
    "/",
    response_model=list[SatelliteResponse],
)
def list_satellites(
    db: Session = Depends(get_db),
):

    satellites = (
        db.query(Satellite)
        .order_by(Satellite.name)
        .all()
    )

    return satellites
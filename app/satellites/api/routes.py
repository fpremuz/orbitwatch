from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.satellites.infrastructure.repository import SatelliteRepository
from app.satellites.api.schemas import (
    SatelliteCreate,
    SatelliteResponse,
)
import uuid

router = APIRouter(prefix="/satellites", tags=["Satellites"])


@router.post("/", response_model=SatelliteResponse)
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


@router.get("/", response_model=list[SatelliteResponse])
def list_satellites(
    db: Session = Depends(get_db),
):
    repo = SatelliteRepository(db)
    return repo.get_all()


@router.get("/{satellite_id}", response_model=SatelliteResponse)
def get_satellite(
    satellite_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    repo = SatelliteRepository(db)
    satellite = repo.get_by_id(satellite_id)

    if not satellite:
        raise HTTPException(status_code=404, detail="Satellite not found")

    return satellite
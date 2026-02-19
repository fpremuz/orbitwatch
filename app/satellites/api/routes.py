from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.satellites.repository.satellite_repository import SatelliteRepository

router = APIRouter(prefix="/satellites", tags=["satellites"])


@router.post("/")
def create_satellite(name: str, norad_id: str | None = None, db: Session = Depends(get_db)):
    repo = SatelliteRepository(db)
    satellite = repo.create(name=name, norad_id=norad_id)
    return satellite
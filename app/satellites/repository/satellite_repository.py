from sqlalchemy.orm import Session
from app.satellites.domain.models import Satellite


class SatelliteRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, norad_id: str | None = None) -> Satellite:
        satellite = Satellite(name=name, norad_id=norad_id)
        self.db.add(satellite)
        self.db.commit()
        self.db.refresh(satellite)
        return satellite

    def get_by_name(self, name: str) -> Satellite | None:
        return (
            self.db.query(Satellite)
            .filter(Satellite.name == name)
            .first()
        )
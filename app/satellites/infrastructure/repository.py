from sqlalchemy.orm import Session
from app.satellites.domain.models import Satellite
import uuid


class SatelliteRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, norad_id: str):
        satellite = Satellite(name=name, norad_id=norad_id)
        self.db.add(satellite)
        self.db.commit()
        self.db.refresh(satellite)
        return satellite

    def get_all(self):
        return self.db.query(Satellite).all()

    def get_by_id(self, satellite_id: uuid.UUID):
        return self.db.query(Satellite).filter(
            Satellite.id == satellite_id
        ).first()
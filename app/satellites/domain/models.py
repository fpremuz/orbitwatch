from uuid import uuid4

from sqlalchemy import (Column, String, Integer)
from sqlalchemy import DateTime, Float

from sqlalchemy.dialects.postgresql import UUID

from app.core.base import Base


class Satellite(Base):

    __tablename__ = "satellites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    norad_id = Column(Integer, unique=True, nullable=False)
    orbit_type = Column(String, nullable=False, default="LEO")
    last_seen_at = Column(DateTime(timezone=True), nullable=True)
    health_score = Column(Float, nullable=False, default=100.0)
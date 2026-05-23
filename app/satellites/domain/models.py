from uuid import uuid4

from sqlalchemy import (Column, String, Integer)

from sqlalchemy.dialects.postgresql import UUID

from app.core.base import Base


class Satellite(Base):

    __tablename__ = "satellites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    norad_id = Column(Integer, unique=True, nullable=False)
    orbit_type = Column(String, nullable=False, default="LEO")
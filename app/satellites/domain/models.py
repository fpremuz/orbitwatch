import uuid
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.base import Base


class Satellite(Base):
    __tablename__ = "satellites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    norad_id = Column(Integer, unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

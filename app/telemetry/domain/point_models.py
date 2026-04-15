import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.core.base import Base


class TelemetryPoint(Base):
    __tablename__ = "telemetry_points"

    __allow_unmapped__ = True  

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    event_id = Column(UUID(as_uuid=True), nullable=False)

    satellite_id = Column(UUID(as_uuid=True), ForeignKey("satellites.id"), nullable=False)
    parameter_id = Column(UUID(as_uuid=True), ForeignKey("telemetry_parameters.id"), nullable=False)

    timestamp = Column(DateTime(timezone=True), nullable=False)
    value = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    parameter_name: str = None
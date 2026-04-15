import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.database import Base


class TelemetryPoint(Base):
    __tablename__ = "telemetry_points"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    event_id = Column(UUID(as_uuid=True), nullable=False)

    satellite_id = Column(
        UUID(as_uuid=True),
        ForeignKey("satellites.id", ondelete="CASCADE"),
        nullable=False,
    )

    parameter_id = Column(
        UUID(as_uuid=True),
        ForeignKey("telemetry_parameters.id", ondelete="CASCADE"),
        nullable=False,
    )

    timestamp = Column(DateTime(timezone=True), nullable=False)

    value = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_sat_param_time", "satellite_id", "parameter_id", "timestamp"),
        UniqueConstraint("event_id", "parameter_id", name="uq_event_parameter"),
    )
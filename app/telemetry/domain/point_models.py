import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class TelemetryPoint(Base):

    __tablename__ = "telemetry_points"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

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


Index(
    "idx_sat_param_time",
    TelemetryPoint.satellite_id,
    TelemetryPoint.parameter_id,
    TelemetryPoint.timestamp,
)
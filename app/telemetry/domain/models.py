import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.base import Base

class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    satellite_id = Column(
        UUID(as_uuid=True),
        ForeignKey("satellites.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    timestamp = Column(DateTime(timezone=True), nullable=False)

    temperature = Column(Float, nullable=False)
    velocity = Column(Float, nullable=False)
    altitude = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


Index(
    "idx_satellite_timestamp",
    Telemetry.satellite_id,
    Telemetry.timestamp.desc(),
)
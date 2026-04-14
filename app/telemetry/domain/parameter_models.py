import uuid
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

__table_args__ = (
    UniqueConstraint("satellite_id", "name", name="uq_satellite_parameter"),
)

class TelemetryParameter(Base):

    __tablename__ = "telemetry_parameters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    satellite_id = Column(
        UUID(as_uuid=True),
        ForeignKey("satellites.id", ondelete="CASCADE"),
        nullable=False,
    )

    name = Column(String, nullable=False)
    unit = Column(String, nullable=True)

    min_value = Column(Float, nullable=True)
    max_value = Column(Float, nullable=True)
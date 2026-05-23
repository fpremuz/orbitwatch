from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, UTC
import uuid

from app.core.base import Base


class AIInsight(Base):
    __tablename__ = "ai_insights"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    satellite_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )

    alert_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )

    summary = Column(Text, nullable=False)

    possible_cause = Column(Text, nullable=False)

    recommendation = Column(Text, nullable=False)

    severity = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
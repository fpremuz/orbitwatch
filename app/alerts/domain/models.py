import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.base import Base


class Alert(Base):

    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    satellite_id = Column(UUID(as_uuid=True), nullable=False)

    parameter = Column(String, nullable=False)

    level = Column(String, nullable=False)

    message = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
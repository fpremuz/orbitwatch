from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class ParameterSchema(BaseModel):

    name: str
    value: float


class TelemetryEventSchema(BaseModel):

    event_id: UUID
    satellite_id: UUID
    timestamp: datetime
    parameters: list[ParameterSchema]
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class TelemetryParameterInput(BaseModel):

    name: str
    value: float


class TelemetryEventCreate(BaseModel):

    satellite_id: UUID
    timestamp: datetime
    parameters: list[TelemetryParameterInput]


class TelemetryEventBatchCreate(BaseModel):

    events: list[TelemetryEventCreate]
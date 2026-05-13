from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TelemetryParameterInput(BaseModel):
    name: str
    value: float


class TelemetryEventCreate(BaseModel):
    satellite_id: UUID
    timestamp: datetime
    parameters: list[TelemetryParameterInput]


class TelemetryEventBatchCreate(BaseModel):
    events: list[TelemetryEventCreate]


class TelemetryHistoryResponse(BaseModel):
    timestamp: datetime
    value: float
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List

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


# ----------------------------
# Ingestion Schemas
# ----------------------------

class TelemetryCreate(BaseModel):

    satellite_id: UUID
    timestamp: datetime
    temperature: float
    velocity: float
    altitude: float


class TelemetryBatchCreate(BaseModel):

    measurements: List[TelemetryCreate]


# ----------------------------
# Response Schema
# ----------------------------

class TelemetryResponse(BaseModel):

    id: UUID
    satellite_id: UUID
    timestamp: datetime
    temperature: float
    velocity: float
    altitude: float

    class Config:
        from_attributes = True
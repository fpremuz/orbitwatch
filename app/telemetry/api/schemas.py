import uuid
from datetime import datetime
from pydantic import BaseModel


class TelemetryCreate(BaseModel):
    satellite_id: uuid.UUID
    temperature: float
    velocity: float
    altitude: float

class TelemetryBatchCreate(BaseModel):
    measurements: list[TelemetryCreate]

class TelemetryResponse(BaseModel):
    id: uuid.UUID
    satellite_id: uuid.UUID
    timestamp: datetime
    temperature: float
    velocity: float
    altitude: float

    class Config:
        from_attributes = True
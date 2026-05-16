from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SatelliteResponse(BaseModel):

    id: UUID
    name: str
    norad_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True
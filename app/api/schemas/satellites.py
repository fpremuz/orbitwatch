from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SatelliteResponse(BaseModel):

    id: UUID
    name: str
    norad_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True
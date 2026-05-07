from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: UUID
    satellite_id: UUID
    parameter: str
    level: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class AlertResponse(BaseModel):

    id: UUID
    satellite_id: UUID
    message: str
    severity: str
    created_at: datetime

    class Config:
        from_attributes = True
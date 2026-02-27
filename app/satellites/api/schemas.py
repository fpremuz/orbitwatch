from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, ConfigDict
import uuid


class SatelliteCreate(BaseModel):
    name: str
    norad_id: str



class SatelliteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    norad_id: str
    created_at: datetime
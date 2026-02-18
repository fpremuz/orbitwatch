from uuid import UUID, uuid4

class SatelliteState:
    satellite_id: UUID
    timestamp: datetime
    position: Optional[GeoPosition]
    attitude: Optional[Attitude]
    mode: SatelliteMode
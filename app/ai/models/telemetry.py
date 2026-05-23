from pydantic import BaseModel

class TelemetryData(BaseModel):
    satellite_id: str
    temperature: float
    battery: float
    signal_strength: float
    orbit_deviation: float
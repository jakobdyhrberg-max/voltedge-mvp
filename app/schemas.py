from pydantic import BaseModel
from typing import Optional

class TelemetryCreate(BaseModel):
    charger_id: str
    location: Optional[str] = "Unknown"
    voltage: float
    current: float
    power: float
    temperature: float
    status: str
    error_code: Optional[str] = None
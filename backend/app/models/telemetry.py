"""
Telemetry data models
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class TelemetryData(BaseModel):
    """Telemetry data payload from sensors"""
    device_id: str = Field(..., description="Unique sensor identifier")
    timestamp: datetime = Field(..., description="UTC timestamp")
    type: Literal["temp", "vibration"] = Field(..., description="Measurement type")
    value: float = Field(..., description="Measurement value")
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "sensor-001",
                "timestamp": "2025-07-14T12:00:00Z",
                "type": "temp",
                "value": 34.5
            }
        }


class TelemetryResponse(BaseModel):
    """Response model for telemetry data"""
    device_id: str
    timestamp: datetime
    type: str
    value: float
    id: str = Field(alias="_id", default=None)
    
    class Config:
        populate_by_name = True

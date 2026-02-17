"""
Sensor models
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class Sensor(BaseModel):
    """Sensor information"""
    device_id: str
    last_seen: datetime


class SensorStatus(BaseModel):
    """Sensor status information"""
    device_id: str
    status: Literal["online", "offline"]
    last_seen: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "sensor-001",
                "status": "online",
                "last_seen": "2025-07-14T12:00:00Z"
            }
        }


class SensorStatusResponse(BaseModel):
    """Response model for sensor status list"""
    sensors: list[SensorStatus]
    total: int

"""
Alert models
"""

from pydantic import BaseModel, Field
from datetime import datetime


class Alert(BaseModel):
    """Alert payload for threshold breaches"""
    device_id: str = Field(..., description="Sensor that triggered alert")
    type: str = Field(..., description="Alert type (temp/vibration)")
    value: float = Field(..., description="Measured value")
    threshold: float = Field(..., description="Threshold that was exceeded")
    timestamp: datetime = Field(..., description="When alert occurred")
    message: str = Field(..., description="Human-readable alert message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "sensor-002",
                "type": "temp",
                "value": 52.3,
                "threshold": 50.0,
                "timestamp": "2025-07-14T12:05:00Z",
                "message": "Temperature exceeded threshold"
            }
        }

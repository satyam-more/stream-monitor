"""
Statistics models
"""

from pydantic import BaseModel, Field
from typing import Optional


class Stats(BaseModel):
    """Statistical data for sensor readings"""
    device_id: str = Field(..., description="Sensor identifier")
    type: Optional[str] = Field(None, description="Measurement type filter")
    min: float = Field(..., description="Minimum value")
    max: float = Field(..., description="Maximum value")
    avg: float = Field(..., description="Average value")
    count: int = Field(..., description="Number of data points")
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "sensor-001",
                "type": "temp",
                "min": 22.5,
                "max": 68.3,
                "avg": 45.2,
                "count": 150
            }
        }

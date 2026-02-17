"""
Sensor status tracking service
"""

from datetime import datetime, timedelta
from typing import Dict, Literal
from app.config import settings


class SensorTracker:
    """Tracks sensor online/offline status based on last seen timestamp"""
    
    def __init__(self):
        # In-memory storage: device_id -> last_seen_timestamp
        self.sensors: Dict[str, datetime] = {}
        self.last_data_time: datetime | None = None
    
    def update_sensor(self, device_id: str, timestamp: datetime):
        """Update sensor's last seen timestamp"""
        self.sensors[device_id] = timestamp
        self.last_data_time = timestamp
    
    def get_sensor_status(self, device_id: str) -> Literal["online", "offline"]:
        """
        Determine if sensor is online or offline
        
        Online: Data received within STREAM_TIMEOUT_SECONDS
        Offline: No data for > STREAM_TIMEOUT_SECONDS
        """
        if device_id not in self.sensors:
            return "offline"
        
        last_seen = self.sensors[device_id]
        time_diff = datetime.utcnow() - last_seen
        
        if time_diff.total_seconds() <= settings.stream_timeout_seconds:
            return "online"
        else:
            return "offline"
    
    def get_all_sensors_status(self) -> Dict[str, Dict]:
        """Get status of all tracked sensors"""
        result = {}
        for device_id, last_seen in self.sensors.items():
            result[device_id] = {
                "device_id": device_id,
                "status": self.get_sensor_status(device_id),
                "last_seen": last_seen
            }
        return result
    
    def is_stream_stopped(self) -> bool:
        """
        Check if global stream has stopped
        
        Returns True if no data received for STREAM_TIMEOUT_SECONDS
        """
        if self.last_data_time is None:
            return False
        
        time_diff = datetime.utcnow() - self.last_data_time
        return time_diff.total_seconds() > settings.stream_timeout_seconds


# Global sensor tracker instance
sensor_tracker = SensorTracker()

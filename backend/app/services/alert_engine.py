"""
Alert engine for detecting threshold breaches
"""

from datetime import datetime
from app.models import Alert, TelemetryData
from app.config import settings


class AlertEngine:
    """Detects and generates alerts for threshold breaches"""
    
    @staticmethod
    def check_thresholds(data: TelemetryData) -> Alert | None:
        """
        Check if telemetry data exceeds thresholds
        
        Returns Alert if threshold exceeded, None otherwise
        """
        alert = None
        
        if data.type == "temp" and data.value > settings.alert_temp_threshold:
            alert = Alert(
                device_id=data.device_id,
                type="temp",
                value=data.value,
                threshold=settings.alert_temp_threshold,
                timestamp=data.timestamp,
                message=f"Temperature {data.value}°C exceeded threshold {settings.alert_temp_threshold}°C"
            )
        
        elif data.type == "vibration" and data.value > settings.alert_vibration_threshold:
            alert = Alert(
                device_id=data.device_id,
                type="vibration",
                value=data.value,
                threshold=settings.alert_vibration_threshold,
                timestamp=data.timestamp,
                message=f"Vibration {data.value}g exceeded threshold {settings.alert_vibration_threshold}g"
            )
        
        return alert


# Global alert engine instance
alert_engine = AlertEngine()

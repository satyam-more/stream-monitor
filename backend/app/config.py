"""
Configuration management for the application
Loads settings from environment variables
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # MongoDB Configuration
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "telemetry_db"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Alert Thresholds
    alert_temp_threshold: float = 50.0
    alert_vibration_threshold: float = 0.08
    
    # Stream Monitoring
    stream_timeout_seconds: int = 10
    
    # CORS - simple list
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

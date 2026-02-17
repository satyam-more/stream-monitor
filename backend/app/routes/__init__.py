"""
API route handlers
"""

from .data import router as data_router
from .sensors import router as sensors_router
from .websocket import router as websocket_router

__all__ = ["data_router", "sensors_router", "websocket_router"]

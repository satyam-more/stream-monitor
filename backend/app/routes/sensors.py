"""
Sensor management API endpoints
"""

from fastapi import APIRouter, Path, Query, HTTPException
from typing import Optional
from datetime import datetime

from app.services import database
from app.services.sensor_tracker import sensor_tracker

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.get("")
async def get_sensors():
    """Get list of all unique sensors"""
    
    print("📊 GET /sensors")
    
    # Get unique sensor IDs from database
    sensors = await database.get_all_sensors()
    
    print(f"✅ Found {len(sensors)} sensors")
    
    return {
        "sensors": sensors,
        "count": len(sensors)
    }


@router.get("/{device_id}")
async def get_sensor_data(
    device_id: str = Path(..., description="Sensor device ID"),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all data for a specific sensor"""
    
    print(f"📊 GET /sensors/{device_id}")
    
    # Get sensor data
    data = await database.get_sensor_data(device_id, limit)
    
    if not data:
        raise HTTPException(status_code=404, detail=f"Sensor {device_id} not found")
    
    # Convert ObjectId and datetime
    result = []
    for item in data:
        item['_id'] = str(item['_id'])
        if isinstance(item['timestamp'], datetime):
            item['timestamp'] = item['timestamp'].isoformat()
        result.append(item)
    
    print(f"✅ Returning {len(result)} records for {device_id}")
    
    return {
        "device_id": device_id,
        "data": result,
        "count": len(result)
    }


@router.get("/status/online")
async def get_online_sensors():
    """Get list of online sensors (data received within 10 seconds)"""
    
    print("📊 GET /sensors/status/online")
    
    # Get all sensor statuses
    all_statuses = sensor_tracker.get_all_sensors_status()
    
    # Filter only online sensors using list comprehension
    online = [s for s in all_statuses.values() if s['status'] == 'online']
    
    # Convert datetime to ISO string
    for sensor in online:
        if isinstance(sensor['last_seen'], datetime):
            sensor['last_seen'] = sensor['last_seen'].isoformat()
    
    print(f"✅ Found {len(online)} online sensors")
    
    return {
        "sensors": online,
        "count": len(online)
    }


@router.get("/status/offline")
async def get_offline_sensors():
    """Get list of offline sensors (no data for > 10 seconds)"""
    
    print("📊 GET /sensors/status/offline")
    
    # Get all sensor statuses
    all_statuses = sensor_tracker.get_all_sensors_status()
    
    # Filter only offline sensors
    offline = [s for s in all_statuses.values() if s['status'] == 'offline']
    
    # Convert datetime to ISO string
    for sensor in offline:
        if isinstance(sensor['last_seen'], datetime):
            sensor['last_seen'] = sensor['last_seen'].isoformat()
    
    print(f"✅ Found {len(offline)} offline sensors")
    
    return {
        "sensors": offline,
        "count": len(offline)
    }


@router.get("/status")
async def get_all_sensor_status():
    """Get status of all sensors (online/offline)"""
    
    print("📊 GET /sensors/status")
    
    # Get all sensor statuses
    all_statuses = sensor_tracker.get_all_sensors_status()
    
    # Convert to list
    sensors = list(all_statuses.values())
    
    # Convert datetime to ISO string
    for sensor in sensors:
        if isinstance(sensor['last_seen'], datetime):
            sensor['last_seen'] = sensor['last_seen'].isoformat()
    
    print(f"✅ Returning status for {len(sensors)} sensors")
    
    return {
        "sensors": sensors,
        "count": len(sensors)
    }

"""
Data retrieval API endpoints
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime

from app.services import database

router = APIRouter(prefix="/data", tags=["data"])


@router.get("")
async def get_data(
    start: Optional[str] = Query(None, description="Start time filter (ISO format)"),
    end: Optional[str] = Query(None, description="End time filter (ISO format)"),
    device_id: Optional[str] = Query(None, description="Filter by device ID"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum results")
):
    """
    Retrieve telemetry data with optional filters
    
    - **start**: Filter data from this timestamp
    - **end**: Filter data until this timestamp
    - **device_id**: Filter by specific sensor
    - **limit**: Maximum number of results (1-1000)
    """
    
    print(f"📊 GET /data - start={start}, end={end}, device_id={device_id}, limit={limit}")
    
    # Parse datetime strings
    start_time = None
    end_time = None
    
    try:
        if start:
            start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
        if end:
            end_time = datetime.fromisoformat(end.replace('Z', '+00:00'))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid datetime format: {e}")
    
    # Get data from database
    data = await database.get_data_in_range(start_time, end_time, device_id, limit)
    
    # Convert ObjectId to string (MongoDB returns ObjectId)
    result = []
    for item in data:
        item['_id'] = str(item['_id'])
        # Convert datetime to ISO string
        if isinstance(item['timestamp'], datetime):
            item['timestamp'] = item['timestamp'].isoformat()
        result.append(item)
    
    print(f"✅ Returning {len(result)} records")
    
    return {
        "data": result,
        "count": len(result)
    }


@router.get("/latest")
async def get_latest_data(limit: int = Query(10, ge=1, le=100)):
    """Get the most recent telemetry readings"""
    
    print(f"📊 GET /data/latest - limit={limit}")
    
    db = database.get_database()
    
    # Get latest data sorted by timestamp
    cursor = db.sensor_data.find().sort("timestamp", -1).limit(limit)
    data = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    result = []
    for item in data:
        item['_id'] = str(item['_id'])
        if isinstance(item['timestamp'], datetime):
            item['timestamp'] = item['timestamp'].isoformat()
        result.append(item)
    
    print(f"✅ Returning {len(result)} latest records")
    
    return {
        "data": result,
        "count": len(result)
    }



@router.get("/stats")
async def get_stats(
    device_id: str = Query(..., description="Sensor device ID"),
    start: Optional[str] = Query(None, description="Start time (ISO format)"),
    end: Optional[str] = Query(None, description="End time (ISO format)"),
    type: Optional[str] = Query(None, description="Filter by type (temp/vibration)")
):
    """
    Get statistics (min, max, avg) for sensor data
    
    - **device_id**: Required sensor ID
    - **start**: Optional start time filter
    - **end**: Optional end time filter
    - **type**: Optional type filter (temp or vibration)
    """
    
    print(f"📊 GET /data/stats - device_id={device_id}, type={type}")
    
    db = database.get_database()
    
    # Build query
    query = {"device_id": device_id}
    
    # Add time filters
    if start or end:
        query["timestamp"] = {}
        if start:
            start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
            query["timestamp"]["$gte"] = start_time
        if end:
            end_time = datetime.fromisoformat(end.replace('Z', '+00:00'))
            query["timestamp"]["$lte"] = end_time
    
    # Add type filter
    if type:
        query["type"] = type
    
    # Get data
    cursor = db.sensor_data.find(query)
    data = await cursor.to_list(length=None)
    
    if not data:
        raise HTTPException(status_code=404, detail="No data found for the given filters")
    
    # Calculate statistics using list comprehension
    values = [item['value'] for item in data]
    
    stats = {
        "device_id": device_id,
        "type": type,
        "min": min(values),
        "max": max(values),
        "avg": round(sum(values) / len(values), 2),
        "count": len(values)
    }
    
    print(f"✅ Stats calculated: min={stats['min']}, max={stats['max']}, avg={stats['avg']}")
    
    return stats

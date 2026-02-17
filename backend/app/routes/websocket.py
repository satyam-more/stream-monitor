"""
WebSocket endpoints for real-time communication
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime
import json

from app.models import TelemetryData, Alert
from app.services.database import insert_telemetry_data, get_database
from app.services.alert_engine import alert_engine
from app.services.sensor_tracker import sensor_tracker

router = APIRouter(tags=["websocket"])

# Store connected frontend clients (global variable - fresher style)
frontend_clients = []


@router.websocket("/stream/data")
async def websocket_data_ingestion(websocket: WebSocket):
    """
    WebSocket endpoint for receiving telemetry data from simulators
    
    Accepts JSON payloads with format:
    {
        "device_id": "sensor-001",
        "timestamp": "2025-07-14T12:00:00Z",
        "type": "temp",
        "value": 34.5
    }
    """
    await websocket.accept()
    print(f"✅ Simulator connected: {websocket.client}")
    
    try:
        while True:
            # Receive data from simulator
            data_str = await websocket.receive_text()
            
            # Parse JSON
            data_dict = json.loads(data_str)
            
            print(f"📥 Received: {data_dict}")
            
            # Validate data using Pydantic model
            try:
                telemetry = TelemetryData(**data_dict)
            except Exception as e:
                print(f"⚠️ Invalid data format: {e}")
                continue
            
            # Convert to dict for MongoDB
            data_to_save = {
                "device_id": telemetry.device_id,
                "timestamp": telemetry.timestamp,
                "type": telemetry.type,
                "value": telemetry.value
            }
            
            # Save to MongoDB
            await insert_telemetry_data(data_to_save)
            
            # Update sensor tracker
            sensor_tracker.update_sensor(telemetry.device_id, telemetry.timestamp)
            
            # Check for alerts
            alert = alert_engine.check_thresholds(telemetry)
            if alert:
                print(f"🚨 ALERT: {alert.message}")
                # Broadcast alert to frontend clients
                await broadcast_to_frontend({
                    "type": "alert",
                    "data": {
                        "device_id": alert.device_id,
                        "type": alert.type,
                        "value": alert.value,
                        "threshold": alert.threshold,
                        "timestamp": alert.timestamp.isoformat(),
                        "message": alert.message
                    }
                })
            
            # Broadcast new data to frontend clients (convert datetime to string)
            await broadcast_to_frontend({
                "type": "new_data",
                "data": {
                    "device_id": telemetry.device_id,
                    "timestamp": telemetry.timestamp.isoformat(),
                    "type": telemetry.type,
                    "value": telemetry.value
                }
            })
            
    except WebSocketDisconnect:
        print(f"❌ Simulator disconnected: {websocket.client}")
    except Exception as e:
        print(f"❌ Error in data ingestion: {e}")
        await websocket.close()


@router.websocket("/ws")
async def websocket_frontend(websocket: WebSocket):
    """
    WebSocket endpoint for pushing real-time updates to frontend
    
    Sends events:
    - new_data: Live telemetry data
    - alert: Threshold breach alerts
    - stream_stopped: No data received for 10 seconds
    - status_update: Sensor online/offline status changes
    """
    await websocket.accept()
    print(f"✅ Frontend client connected: {websocket.client}")
    
    # Add to connected clients list
    frontend_clients.append(websocket)
    
    try:
        # Keep connection alive
        while True:
            # Wait for messages (ping/pong)
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        print(f"❌ Frontend client disconnected: {websocket.client}")
        # Remove from clients list
        if websocket in frontend_clients:
            frontend_clients.remove(websocket)
    except Exception as e:
        print(f"❌ Error in frontend websocket: {e}")
        if websocket in frontend_clients:
            frontend_clients.remove(websocket)
        await websocket.close()


async def broadcast_to_frontend(message):
    """Send message to all connected frontend clients"""
    # Convert message to JSON string
    message_str = json.dumps(message)
    
    # Send to all clients
    disconnected = []
    for client in frontend_clients:
        try:
            await client.send_text(message_str)
        except:
            # Client disconnected
            disconnected.append(client)
    
    # Remove disconnected clients
    for client in disconnected:
        frontend_clients.remove(client)
    
    if len(frontend_clients) > 0:
        print(f"📤 Broadcasted to {len(frontend_clients)} frontend client(s)")

"""
IoT Sensor Data Simulator
Sends telemetry data to backend via WebSocket
"""

import asyncio
import websockets
import json
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL", "ws://localhost:8000/stream/data")
SEND_INTERVAL = int(os.getenv("SEND_INTERVAL", "1"))

# Sensor IDs
SENSORS = ["sensor-001", "sensor-002", "sensor-003"]


def generate_telemetry_data():
    """Generate random telemetry data"""
    # Pick random sensor
    device_id = random.choice(SENSORS)
    
    # Pick random type
    data_type = random.choice(["temp", "vibration"])
    
    # Generate value based on type
    if data_type == "temp":
        # Temperature range: 20-70
        value = round(random.uniform(20, 70), 2)
    else:
        # Vibration range: 0.01-0.12
        value = round(random.uniform(0.01, 0.12), 3)
    
    # Create payload
    payload = {
        "device_id": device_id,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": data_type,
        "value": value
    }
    
    return payload


async def send_data():
    """Connect to WebSocket and send data continuously"""
    print(f"Connecting to {WEBSOCKET_URL}...")
    
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("✅ Connected to backend!")
            print(f"Simulating {len(SENSORS)} sensors: {', '.join(SENSORS)}")
            print(f"Sending data every {SEND_INTERVAL} second(s)")
            print("-" * 50)
            
            while True:
                # Generate data
                data = generate_telemetry_data()
                
                # Send to backend
                await websocket.send(json.dumps(data))
                
                # Print for debugging
                print(f"📤 Sent: {data['device_id']} | {data['type']} = {data['value']}")
                
                # Wait before sending next
                await asyncio.sleep(SEND_INTERVAL)
                
    except websockets.exceptions.WebSocketException as e:
        print(f"❌ WebSocket error: {e}")
        print("Retrying in 5 seconds...")
        await asyncio.sleep(5)
        # TODO: Add reconnection logic
        
    except KeyboardInterrupt:
        print("\n🛑 Simulator stopped by user")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main entry point"""
    print("=" * 50)
    print("🚀 IoT Sensor Simulator Starting...")
    print("=" * 50)
    
    try:
        # Run the async function
        asyncio.run(send_data())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()

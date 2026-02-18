"""
Simulator Web Control Panel
Simple Flask app to control the IoT simulator
"""

from flask import Flask, render_template, jsonify
import threading
import asyncio
import websockets
import json
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL", "ws://localhost:8000/stream/data")
SEND_INTERVAL = int(os.getenv("SEND_INTERVAL", "1"))
SENSORS = ["sensor-001", "sensor-002", "sensor-003"]

# Global state
simulator_running = False
simulator_thread = None
stats = {
    "messages_sent": 0,
    "connection_status": "Disconnected",
    "last_message": None,
    "errors": 0
}


def generate_telemetry_data():
    """Generate random telemetry data"""
    device_id = random.choice(SENSORS)
    data_type = random.choice(["temp", "vibration"])
    
    if data_type == "temp":
        value = round(random.uniform(20, 70), 2)
    else:
        value = round(random.uniform(0.01, 0.12), 3)
    
    payload = {
        "device_id": device_id,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": data_type,
        "value": value
    }
    
    return payload


async def run_simulator():
    """Run the simulator loop"""
    global stats, simulator_running
    
    while simulator_running:
        try:
            stats["connection_status"] = "Connecting..."
            
            async with websockets.connect(WEBSOCKET_URL) as websocket:
                stats["connection_status"] = "Connected"
                
                while simulator_running:
                    # Generate and send data
                    data = generate_telemetry_data()
                    await websocket.send(json.dumps(data))
                    
                    # Update stats
                    stats["messages_sent"] += 1
                    stats["last_message"] = data
                    
                    # Wait before sending next
                    await asyncio.sleep(SEND_INTERVAL)
                    
        except Exception as e:
            stats["connection_status"] = f"Error: {str(e)}"
            stats["errors"] += 1
            if simulator_running:
                await asyncio.sleep(5)  # Wait before reconnecting
        
    stats["connection_status"] = "Stopped"


def simulator_worker():
    """Thread worker to run async simulator"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_simulator())


@app.route('/')
def index():
    """Main control panel page"""
    return render_template('index.html')


@app.route('/api/start', methods=['POST'])
def start_simulator():
    """Start the simulator"""
    global simulator_running, simulator_thread
    
    if not simulator_running:
        simulator_running = True
        simulator_thread = threading.Thread(target=simulator_worker, daemon=True)
        simulator_thread.start()
        return jsonify({"status": "started", "message": "Simulator started successfully"})
    else:
        return jsonify({"status": "already_running", "message": "Simulator is already running"})


@app.route('/api/stop', methods=['POST'])
def stop_simulator():
    """Stop the simulator"""
    global simulator_running
    
    if simulator_running:
        simulator_running = False
        return jsonify({"status": "stopped", "message": "Simulator stopped successfully"})
    else:
        return jsonify({"status": "already_stopped", "message": "Simulator is not running"})


@app.route('/api/status')
def get_status():
    """Get simulator status"""
    return jsonify({
        "running": simulator_running,
        "stats": stats,
        "config": {
            "websocket_url": WEBSOCKET_URL,
            "send_interval": SEND_INTERVAL,
            "sensors": SENSORS
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "simulator_running": simulator_running})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

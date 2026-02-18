# Stream Monitor

Real-time IoT telemetry streaming system with Python FastAPI backend, React dashboard, and MongoDB storage.

## 🌐 Live Demo

**🎯 Try it now - All services are deployed and running!**

- **📊 Frontend Dashboard:** [https://stream-monitor-web.netlify.app/](https://stream-monitor-web.netlify.app/)
- **🔧 Backend API:** [https://stream-monitor-a4cr.onrender.com](https://stream-monitor-a4cr.onrender.com)
- **📡 API Documentation:** [https://stream-monitor-a4cr.onrender.com/docs](https://stream-monitor-a4cr.onrender.com/docs)
- **🎮 Simulator Control Panel:** [https://stream-monitor-simulator.onrender.com](https://stream-monitor-simulator.onrender.com)

### Quick Start Demo:
1. Open the [Simulator Control Panel](https://stream-monitor-simulator.onrender.com)
2. Click the **"▶ START"** button
3. Open the [Frontend Dashboard](https://your-app.netlify.app)
4. Watch real-time data flow! 🚀

---

## 🚀 Features

- ✅ **Real-time Data Streaming** - WebSocket-based live telemetry updates
- ✅ **Interactive Dashboard** - React-based UI with live charts and visualizations
- ✅ **Web-Based Simulator** - Control panel with start/stop buttons and live statistics
- ✅ **Smart Alerts** - Automatic notifications for threshold breaches
  - Temperature > 50°C
  - Vibration > 0.08g
  - Stream timeout detection (10 seconds)
- ✅ **REST API** - Comprehensive endpoints for data retrieval and analytics
- ✅ **MongoDB Storage** - Efficient time-series data storage with indexing
- ✅ **Fully Deployed** - Backend on Render, Frontend on Netlify, Simulator on Render

## 🏗️ Architecture

```
stream-monitor/
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── config.py         # Configuration
│   │   ├── models/           # Pydantic models
│   │   ├── routes/           # API endpoints
│   │   ├── services/         # Business logic
│   │   └── websocket/        # WebSocket handler
│   └── requirements.txt
│
├── frontend/         # React dashboard
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API & WebSocket clients
│   │   └── App.jsx           # Main application
│   └── package.json
│
└── simulator/        # Data simulator
    ├── simulator.py          # Main simulator script
    └── requirements.txt
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.8+)
- **Database**: MongoDB
- **Real-time**: WebSocket (Socket.io)
- **Validation**: Pydantic

### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite
- **Charts**: Recharts
- **Real-time**: Socket.io-client
- **HTTP Client**: Axios

### Simulator
- **Language**: Python 3.8+
- **Protocol**: WebSocket

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- MongoDB (local or MongoDB Atlas)
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/satyam-more/stream-monitor.git
cd stream-monitor
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your MongoDB connection string

# Run the backend
python app/main.py
```

Backend will run on `http://localhost:8000`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on `http://localhost:5173`

### 4. Simulator Setup
```bash
cd simulator

# Install dependencies
pip install -r requirements.txt

# Run the simulator
python simulator.py
```

## 📡 API Endpoints

### Data Endpoints
- `GET /api/data` - Fetch telemetry data with filters
  - Query params: `startTime`, `endTime`, `sensorId`, `limit`
- `GET /api/data/latest` - Get latest readings

### Sensor Endpoints
- `GET /api/sensors` - List all sensors
- `GET /api/sensors/:id` - Get specific sensor details
- `GET /api/sensors/:id/stats` - Get sensor statistics (min/max/avg)
- `GET /api/sensors/status/online` - List online sensors
- `GET /api/sensors/status/offline` - List offline sensors

### WebSocket Events
- `connect` - Client connection established
- `telemetry_data` - Real-time sensor data
- `alert` - Threshold breach notification
- `stream_stopped` - No data received for 10 seconds

## 📊 Data Format

### Telemetry Payload
```json
{
  "device_id": "sensor-001",
  "timestamp": "2025-07-14T12:00:00Z",
  "type": "temperature",
  "value": 45.5
}
```

### Alert Payload
```json
{
  "device_id": "sensor-002",
  "type": "temperature",
  "value": 52.3,
  "threshold": 50,
  "timestamp": "2025-07-14T12:05:00Z",
  "message": "Temperature exceeded threshold"
}
```

## 🔧 Configuration

### Backend (.env)
```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=telemetry_db
WEBSOCKET_PORT=8000
ALERT_TEMP_THRESHOLD=50
ALERT_VIBRATION_THRESHOLD=0.08
STREAM_TIMEOUT=10
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📦 Deployment

### Using Docker (Recommended)
```bash
# Build and run all services
docker-compose up -d
```

### Manual Deployment
- Backend: Deploy to Heroku, Railway, or AWS
- Frontend: Deploy to Vercel, Netlify, or AWS S3
- Database: Use MongoDB Atlas

## 📈 Development Roadmap

- [x] Project setup and architecture
- [x] Backend API implementation
- [x] MongoDB integration
- [x] WebSocket real-time streaming
- [x] Alert system
- [x] Data simulator with web GUI
- [x] React dashboard
- [x] Charts and visualizations
- [x] Deployment to cloud (Render + Netlify)
- [x] API documentation (Swagger)
- [ ] Unit tests
- [ ] Docker containerization

## 🌐 Deployment

### Live Services

All services are deployed and accessible:

| Service | URL | Status |
|---------|-----|--------|
| **Frontend** | [https://stream-monitor-web.netlify.app/](https://stream-monitor-web.netlify.app/) | ✅ Live |
| **Backend API** | [https://stream-monitor-a4cr.onrender.com](https://stream-monitor-a4cr.onrender.com) | ✅ Live |
| **API Docs** | [https://stream-monitor-a4cr.onrender.com/docs](https://stream-monitor-a4cr.onrender.com/docs) | ✅ Live |
| **Simulator** | [https://stream-monitor-simulator.onrender.com](https://stream-monitor-simulator.onrender.com) | ✅ Live |

### Deployment Stack

- **Frontend:** Netlify (React + Vite + TypeScript)
- **Backend:** Render (Python + FastAPI + WebSocket)
- **Simulator:** Render (Python + Flask + WebSocket Client)
- **Database:** MongoDB Atlas (Cloud)

### How to Use the Deployed System

1. **Start the Simulator:**
   - Visit: https://stream-monitor-simulator.onrender.com
   - Click the green **"▶ START"** button
   - Watch the connection status turn green
   - See real-time statistics (messages sent, errors)

2. **View the Dashboard:**
   - Visit: https://your-app.netlify.app
   - You should see "WebSocket: Connected" in green
   - Real-time data will appear in the Live Table
   - Alerts will show when thresholds are exceeded

3. **Explore the API:**
   - Visit: https://stream-monitor-a4cr.onrender.com/docs
   - Try out the interactive API documentation
   - Test endpoints directly from the browser

### Note on Free Tier
- Services may sleep after 15 minutes of inactivity
- First request takes 30-60 seconds to wake up
- This is normal for free tier hosting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Satyam More**
- GitHub: [@satyam-more](https://github.com/satyam-more)

## 🙏 Acknowledgments

Built as part of YantraMedhavi India Private Limited technical assessment.

---

**⭐ If you find this project useful, please consider giving it a star!**

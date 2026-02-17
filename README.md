# Stream Monitor

Real-time IoT telemetry streaming system with Python FastAPI backend, React dashboard, and MongoDB storage.

## 🚀 Features

- ✅ **Real-time Data Streaming** - WebSocket-based live telemetry updates
- ✅ **Interactive Dashboard** - React-based UI with live charts and visualizations
- ✅ **Smart Alerts** - Automatic notifications for threshold breaches
  - Temperature > 50°C
  - Vibration > 0.08g
  - Stream timeout detection (10 seconds)
- ✅ **REST API** - Comprehensive endpoints for data retrieval and analytics
- ✅ **MongoDB Storage** - Efficient time-series data storage with indexing
- ✅ **Data Simulator** - Python-based telemetry data generator

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
- [ ] Backend API implementation
- [ ] MongoDB integration
- [ ] WebSocket real-time streaming
- [ ] Alert system
- [ ] Data simulator
- [ ] React dashboard
- [ ] Charts and visualizations
- [ ] Unit tests
- [ ] Docker containerization
- [ ] API documentation (Swagger)
- [ ] Deployment

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

"""
FastAPI main application
Stream Monitor - Real-time Telemetry System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.services import database
from app.routes import data_router, sensors_router, websocket_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("=" * 50)
    print("🚀 Starting Stream Monitor Backend...")
    print("=" * 50)
    
    # Connect to MongoDB
    await database.connect_to_mongodb(settings.mongodb_uri, settings.database_name)
    
    print(f"✅ Server running on {settings.host}:{settings.port}")
    print("=" * 50)
    
    yield
    
    # Shutdown
    print("\n" + "=" * 50)
    print("🛑 Shutting down Stream Monitor Backend...")
    await database.disconnect_from_mongodb()
    print("✅ Shutdown complete")
    print("=" * 50)


# Initialize FastAPI application
app = FastAPI(
    title="Stream Monitor API",
    description="Real-time telemetry streaming system with WebSocket support",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(data_router, prefix="/api")
app.include_router(sensors_router, prefix="/api")
app.include_router(websocket_router)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Stream Monitor API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db = database.get_database()
    
    return {
        "status": "healthy",
        "database": "connected" if db else "disconnected (running in demo mode)"
    }


if __name__ == "__main__":
    import uvicorn
    
    print("Starting server...")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )

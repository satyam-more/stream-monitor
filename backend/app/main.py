"""
FastAPI main application
Stream Monitor - Real-time Telemetry System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.services.database import db_service
from app.routes import data_router, sensors_router, websocket_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting Stream Monitor Backend...")
    await db_service.connect(settings.mongodb_uri, settings.database_name)
    print(f"✅ Server running on {settings.host}:{settings.port}")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Stream Monitor Backend...")
    await db_service.disconnect()
    print("✅ Shutdown complete")


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
    allow_origins=settings.cors_origins,
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
    return {
        "status": "healthy",
        "database": "connected" if db_service.db else "disconnected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )

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
    
    # Connect to MongoDB (non-blocking, won't crash if fails)
    try:
        await database.connect_to_mongodb(settings.mongodb_uri, settings.database_name)
    except Exception as e:
        print(f"⚠️ MongoDB connection failed during startup: {e}")
        print("⚠️ Continuing without database...")
    
    print(f"✅ Server running on {settings.host}:{settings.port}")
    print("=" * 50)
    
    yield
    
    # Shutdown
    print("\n" + "=" * 50)
    print("🛑 Shutting down Stream Monitor Backend...")
    try:
        await database.disconnect_from_mongodb()
    except Exception as e:
        print(f"⚠️ Error during shutdown: {e}")
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
    try:
        db = database.get_database()
        
        # Try to ping database if connected
        db_status = "disconnected"
        if db:
            try:
                await db.command('ping')
                db_status = "connected"
            except:
                db_status = "error"
        
        return {
            "status": "healthy",
            "database": db_status,
            "message": "Backend is running" if not db else "Backend is running with database"
        }
    except Exception as e:
        # Even if there's an error, return 200 to show backend is alive
        return {
            "status": "healthy",
            "database": "unknown",
            "message": f"Backend is running (health check error: {str(e)})"
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

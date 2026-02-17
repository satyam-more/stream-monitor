"""
Database service for MongoDB operations
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional


class DatabaseService:
    """Handles all MongoDB operations"""
    
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    
    @classmethod
    async def connect(cls, mongodb_uri: str, database_name: str):
        """Connect to MongoDB and create indexes"""
        print(f"Connecting to MongoDB: {mongodb_uri}")
        cls.client = AsyncIOMotorClient(mongodb_uri)
        cls.db = cls.client[database_name]
        
        # Create indexes for efficient queries
        await cls.create_indexes()
        print("MongoDB connected successfully")
    
    @classmethod
    async def create_indexes(cls):
        """Create database indexes for optimal query performance"""
        if cls.db is None:
            return
        
        # Indexes on sensor_data collection
        await cls.db.sensor_data.create_index("device_id")
        await cls.db.sensor_data.create_index("timestamp")
        await cls.db.sensor_data.create_index("type")
        await cls.db.sensor_data.create_index([("device_id", 1), ("timestamp", -1)])
        
        print("Database indexes created")
    
    @classmethod
    async def disconnect(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            print("MongoDB disconnected")
    
    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """Get database instance"""
        if cls.db is None:
            raise RuntimeError("Database not connected")
        return cls.db


# Global database service instance
db_service = DatabaseService()

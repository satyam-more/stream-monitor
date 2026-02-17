"""
Database service for MongoDB operations
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

# Global variables (fresher style)
client = None
db = None


async def connect_to_mongodb(mongodb_uri: str, database_name: str):
    """Connect to MongoDB and create indexes"""
    global client, db
    
    print(f"🔌 Connecting to MongoDB...")
    print(f"URI: {mongodb_uri}")
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongodb_uri)
        db = client[database_name]
        
        # Test connection
        await db.command('ping')
        print("✅ MongoDB connected successfully!")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        print(f"⚠️ MongoDB connection failed: {e}")
        print("⚠️ Running in NO-DATABASE mode (data will not be saved)")
        print("⚠️ This is OK for demonstration purposes")
        # Don't raise - allow backend to start without MongoDB
        client = None
        db = None


async def create_indexes():
    """Create database indexes for better performance"""
    global db
    
    if db is None:
        print("⚠️ Database not connected, skipping index creation")
        return
    
    print("📊 Creating database indexes...")
    
    # Create indexes on sensor_data collection
    await db.sensor_data.create_index("device_id")
    await db.sensor_data.create_index("timestamp")
    await db.sensor_data.create_index("type")
    
    # Compound index for queries
    await db.sensor_data.create_index([("device_id", 1), ("timestamp", -1)])
    
    print("✅ Indexes created!")


async def disconnect_from_mongodb():
    """Close MongoDB connection"""
    global client
    
    if client:
        client.close()
        print("👋 MongoDB disconnected")


def get_database():
    """Get database instance"""
    global db
    
    if db is None:
        print("⚠️ Database not connected - returning None")
        return None
    
    return db


# Helper functions for common operations
async def insert_telemetry_data(data):
    """Insert telemetry data into database"""
    global db
    
    if db is None:
        print(f"⚠️ No database - skipping save: {data['device_id']} | {data['type']} = {data['value']}")
        return None
    
    # Insert into sensor_data collection
    result = await db.sensor_data.insert_one(data)
    
    # Print for debugging
    print(f"💾 Saved to DB: {data['device_id']} | {data['type']} = {data['value']}")
    
    return result


async def get_all_sensors():
    """Get list of unique sensor IDs"""
    global db
    
    if db is None:
        # Return mock data when no database
        return ["sensor-001", "sensor-002", "sensor-003"]
    
    # Using distinct to get unique device_ids
    sensors = await db.sensor_data.distinct("device_id")
    
    return sensors


async def get_sensor_data(device_id: str, limit: int = 100):
    """Get data for specific sensor"""
    db = get_database()
    
    # Query and sort by timestamp
    cursor = db.sensor_data.find({"device_id": device_id}).sort("timestamp", -1).limit(limit)
    
    # Convert to list
    data = await cursor.to_list(length=limit)
    
    return data


async def get_data_in_range(start_time, end_time, device_id=None, limit=100):
    """Get data within time range"""
    db = get_database()
    
    # Build query
    query = {}
    
    if start_time or end_time:
        query["timestamp"] = {}
        if start_time:
            query["timestamp"]["$gte"] = start_time
        if end_time:
            query["timestamp"]["$lte"] = end_time
    
    if device_id:
        query["device_id"] = device_id
    
    # Execute query
    cursor = db.sensor_data.find(query).sort("timestamp", -1).limit(limit)
    data = await cursor.to_list(length=limit)
    
    return data

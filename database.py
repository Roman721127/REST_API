import motor.motor_asyncio
import os
import certifi

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo_admin:password@localhost:27017")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())
db = client.library

async def get_db():
    yield db
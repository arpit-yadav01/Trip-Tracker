from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DB_NAME]

users_collection = db["users"]
trips_collection = db["trips"]
sos_collection = db["sos_events"]

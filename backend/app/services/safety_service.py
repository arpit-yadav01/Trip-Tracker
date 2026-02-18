from datetime import datetime
from bson import ObjectId
from app.db.mongo import sos_collection, trips_collection


async def create_safety_event(trip_id: str, user_id: str, offline_minutes: int):

    # Fetch last known location
    trip = await trips_collection.find_one({"_id": ObjectId(trip_id)})

    last_location = None

    if trip and "live_locations" in trip:
        last_location = trip["live_locations"].get(user_id)

    event = {
        "trip_id": ObjectId(trip_id),
        "user_id": user_id,
        "offline_minutes": offline_minutes,
        "last_location": last_location,
        "triggered_at": datetime.utcnow(),
        "status": "TRIGGERED"
    }

    await sos_collection.insert_one(event)

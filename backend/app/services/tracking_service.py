from bson import ObjectId
from app.db.mongo import trips_collection

async def update_location_service(trip_id: str, user_id: str, lat: float, lng: float, timestamp: int):
    await trips_collection.update_one(
        {"_id": ObjectId(trip_id)},
        {
            "$set": {
                f"live_locations.{user_id}": {
                    "lat": lat,
                    "lng": lng,
                    "timestamp": timestamp
                }
            }
        }
    )

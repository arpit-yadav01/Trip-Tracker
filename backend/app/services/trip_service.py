from bson import ObjectId
from app.db.mongo import trips_collection
from app.models.trip import trip_model


async def create_trip_service(data: dict):
    trip_data = trip_model(data)
    result = await trips_collection.insert_one(trip_data)

    return {
        "trip_id": str(result.inserted_id),
        "status": trip_data["status"]
    }


async def join_trip_service(trip_id: str, user_id: str):
    trip = await trips_collection.find_one({"_id": ObjectId(trip_id)})

    if not trip:
        return None

    if user_id not in trip["members"]:
        await trips_collection.update_one(
            {"_id": ObjectId(trip_id)},
            {"$push": {"members": user_id}}
        )

    return True


async def activate_trip_service(trip_id: str):
    await trips_collection.update_one(
        {"_id": ObjectId(trip_id)},
        {"$set": {"status": "ACTIVE"}}
    )

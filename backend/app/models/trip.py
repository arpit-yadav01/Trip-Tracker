from datetime import datetime

def trip_model(data: dict):
    return {
        "leader_id": data["leader_id"],
        "destination": {
            "name": data["destination_name"],
            "lat": data["destination_lat"],
            "lng": data["destination_lng"],
        },
        "members": [data["leader_id"]],
        "live_locations": {},  # ✅ NEW FIELD
        "status": "CREATED",
        "offline_threshold_minutes": data.get("offline_threshold_minutes", 60),
        "chat_persistence": data.get("chat_persistence", False),
        "created_at": datetime.utcnow(),
    }

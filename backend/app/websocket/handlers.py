from fastapi import WebSocket, WebSocketDisconnect
from bson import ObjectId
from app.core.security import verify_token
from app.db.mongo import trips_collection
from app.websocket.manager import manager
from app.services.tracking_service import update_location_service


async def handle_websocket(websocket: WebSocket, trip_id: str, token: str):

    # 1️⃣ Verify JWT
    payload = verify_token(token)
    if not payload:
        await websocket.close(code=1008)
        return

    user_id = payload.get("sub")

    # 2️⃣ Verify trip exists
    trip = await trips_collection.find_one({"_id": ObjectId(trip_id)})
    if not trip:
        await websocket.close(code=1008)
        return

    # 3️⃣ Check ACTIVE
    if trip["status"] != "ACTIVE":
        await websocket.close(code=1008)
        return

    # 4️⃣ Check membership
    if user_id not in trip["members"]:
        await websocket.close(code=1008)
        return

    # 5️⃣ Connect
    await manager.connect(trip_id, user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")

            # =========================
            # LOCATION UPDATE
            # =========================
            if event_type == "location_update":

                lat = data.get("lat")
                lng = data.get("lng")
                timestamp = data.get("timestamp")

                if lat is None or lng is None:
                    continue

                await update_location_service(
                    trip_id=trip_id,
                    user_id=user_id,
                    lat=lat,
                    lng=lng,
                    timestamp=timestamp
                )

                await manager.broadcast(trip_id, {
                    "type": "member_location",
                    "user_id": user_id,
                    "lat": lat,
                    "lng": lng,
                    "timestamp": timestamp
                })

            # =========================
            # HEARTBEAT
            # =========================
            elif event_type == "heartbeat":

                manager.update_heartbeat(trip_id, user_id)

                await manager.broadcast(trip_id, {
                    "type": "member_online",
                    "user_id": user_id
                })

    except WebSocketDisconnect:
        manager.disconnect(trip_id, user_id, websocket)

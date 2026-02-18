from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from bson import ObjectId

from app.websocket.manager import manager
from app.core.security import verify_token
from app.db.mongo import trips_collection
from app.api import auth, trips


app = FastAPI()

# Include REST routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(trips.router, prefix="/trips", tags=["Trips"])


@app.websocket("/ws/{trip_id}")
async def websocket_endpoint(websocket: WebSocket, trip_id: str, token: str):

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

    # 3️⃣ Check trip ACTIVE
    if trip["status"] != "ACTIVE":
        await websocket.close(code=1008)
        return

    # 4️⃣ Check membership
    if user_id not in trip["members"]:
        await websocket.close(code=1008)
        return

    # 5️⃣ Accept connection
    await manager.connect(trip_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            data["user_id"] = user_id
            await manager.broadcast(trip_id, data)


    except WebSocketDisconnect:
        manager.disconnect(trip_id, websocket)

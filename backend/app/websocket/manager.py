import time
import asyncio
from fastapi import WebSocket
from typing import Dict, List
from bson import ObjectId
from app.db.mongo import trips_collection
from app.services.safety_service import create_safety_event


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

        # trip_id -> user_id -> presence data
        self.presence: Dict[str, Dict[str, dict]] = {}

    # =============================
    # CONNECT
    # =============================
    async def connect(self, trip_id: str, user_id: str, websocket: WebSocket):
        await websocket.accept()

        if trip_id not in self.active_connections:
            self.active_connections[trip_id] = []

        if trip_id not in self.presence:
            self.presence[trip_id] = {}

        self.active_connections[trip_id].append(websocket)

        # Initialize presence state
        self.presence[trip_id][user_id] = {
            "last_seen": time.time(),
            "offline_since": None,
            "safety_triggered": False
        }

    # =============================
    # DISCONNECT
    # =============================
    def disconnect(self, trip_id: str, user_id: str, websocket: WebSocket):
        if trip_id in self.active_connections:
            if websocket in self.active_connections[trip_id]:
                self.active_connections[trip_id].remove(websocket)

    # =============================
    # HEARTBEAT UPDATE
    # =============================
    def update_heartbeat(self, trip_id: str, user_id: str):
        if trip_id in self.presence and user_id in self.presence[trip_id]:
            self.presence[trip_id][user_id]["last_seen"] = time.time()
            self.presence[trip_id][user_id]["offline_since"] = None

    # =============================
    # BROADCAST
    # =============================
    async def broadcast(self, trip_id: str, message: dict):
        for connection in self.active_connections.get(trip_id, []):
            await connection.send_json(message)

    # =============================
    # MONITOR PRESENCE
    # =============================
    async def monitor_presence(self):
        while True:
            now = time.time()

            for trip_id in list(self.presence.keys()):

                # Fetch trip from DB
                trip = await trips_collection.find_one(
                    {"_id": ObjectId(trip_id)}
                )

                if not trip or trip["status"] != "ACTIVE":
                    continue

                threshold_seconds = (
                    trip.get("offline_threshold_minutes", 60) * 60
                )

                for user_id, data in list(self.presence[trip_id].items()):

                    last_seen = data["last_seen"]

                    # =============================
                    # SHORT OFFLINE (UI layer)
                    # =============================
                    if now - last_seen > 30:

                        if data["offline_since"] is None:
                            data["offline_since"] = now

                            await self.broadcast(trip_id, {
                                "type": "member_offline",
                                "user_id": user_id
                            })

                    # =============================
                    # LONG OFFLINE (SAFETY layer)
                    # =============================
                    if data["offline_since"]:

                        offline_duration = now - data["offline_since"]

                        if (
                            offline_duration > threshold_seconds
                            and not data["safety_triggered"]
                        ):
                            data["safety_triggered"] = True

                            offline_minutes = int(offline_duration / 60)

                            # Persist safety event
                            await create_safety_event(
                                trip_id=trip_id,
                                user_id=user_id,
                                offline_minutes=offline_minutes
                            )

                            # Broadcast safety trigger
                            await self.broadcast(trip_id, {
                                "type": "safety_trigger",
                                "user_id": user_id,
                                "offline_minutes": offline_minutes
                            })

            await asyncio.sleep(5)


manager = ConnectionManager()

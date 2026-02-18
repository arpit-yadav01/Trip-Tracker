from fastapi import WebSocket
from typing import Dict, List
import time
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.presence: Dict[str, Dict[str, float]] = {}  # trip_id → {user_id: last_seen}

    async def connect(self, trip_id: str, user_id: str, websocket: WebSocket):
        await websocket.accept()

        if trip_id not in self.active_connections:
            self.active_connections[trip_id] = []

        if trip_id not in self.presence:
            self.presence[trip_id] = {}

        self.active_connections[trip_id].append(websocket)
        self.presence[trip_id][user_id] = time.time()

    def disconnect(self, trip_id: str, user_id: str, websocket: WebSocket):
        if trip_id in self.active_connections:
            if websocket in self.active_connections[trip_id]:
                self.active_connections[trip_id].remove(websocket)

        if trip_id in self.presence:
            self.presence[trip_id].pop(user_id, None)

    async def broadcast(self, trip_id: str, message: dict):
        for connection in self.active_connections.get(trip_id, []):
            await connection.send_json(message)

    def update_heartbeat(self, trip_id: str, user_id: str):
        if trip_id in self.presence:
            self.presence[trip_id][user_id] = time.time()

    async def monitor_presence(self):
        while True:
            now = time.time()

            for trip_id in list(self.presence.keys()):
                for user_id in list(self.presence[trip_id].keys()):
                    last_seen = self.presence[trip_id][user_id]

                    # 30 seconds timeout
                    if now - last_seen > 30:
                        await self.broadcast(trip_id, {
                            "type": "member_offline",
                            "user_id": user_id
                        })

                        self.presence[trip_id].pop(user_id)

            await asyncio.sleep(5)


manager = ConnectionManager()

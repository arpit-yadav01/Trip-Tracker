from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, trip_id: str, websocket: WebSocket):
        await websocket.accept()

        if trip_id not in self.active_connections:
            self.active_connections[trip_id] = []

        self.active_connections[trip_id].append(websocket)

    def disconnect(self, trip_id: str, websocket: WebSocket):
        if trip_id in self.active_connections:
            self.active_connections[trip_id].remove(websocket)

    async def broadcast(self, trip_id: str, message: dict):
        connections = self.active_connections.get(trip_id, [])

        for connection in connections:
            await connection.send_json(message)


manager = ConnectionManager()

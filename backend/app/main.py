from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.api import auth, trips
from app.websocket.manager import manager
from app.websocket.handlers import handle_websocket
import asyncio

app = FastAPI()

# Include REST routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(trips.router, prefix="/trips", tags=["Trips"])


@app.websocket("/ws/{trip_id}")
async def websocket_endpoint(websocket: WebSocket, trip_id: str, token: str):
    await handle_websocket(websocket, trip_id, token)


# Start presence monitor
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(manager.monitor_presence())

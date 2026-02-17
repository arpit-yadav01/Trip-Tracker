from pydantic import BaseModel
from typing import Optional


class TripCreateRequest(BaseModel):
    leader_id: str
    destination_name: str
    destination_lat: float
    destination_lng: float
    offline_threshold_minutes: Optional[int] = 60
    chat_persistence: Optional[bool] = False


class TripResponse(BaseModel):
    trip_id: str
    status: str


class JoinTripRequest(BaseModel):
    trip_id: str
    user_id: str

from fastapi import APIRouter, HTTPException
from app.schemas.trip import (
    TripCreateRequest,
    TripResponse,
    JoinTripRequest
)
from app.services.trip_service import (
    create_trip_service,
    join_trip_service
)

router = APIRouter()


@router.post("/create", response_model=TripResponse)
async def create_trip(payload: TripCreateRequest):
    result = await create_trip_service(payload.dict())
    return result


@router.post("/join")
async def join_trip(payload: JoinTripRequest):
    success = await join_trip_service(payload.trip_id, payload.user_id)

    if not success:
        raise HTTPException(status_code=404, detail="Trip not found")

    return {"message": "Joined trip successfully"}

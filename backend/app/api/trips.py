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

from app.schemas.trip import ActivateTripRequest
from app.services.trip_service import activate_trip_service
from fastapi import HTTPException

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


@router.post("/activate")
async def activate_trip(payload: ActivateTripRequest):
    result = await activate_trip_service(
        payload.trip_id,
        payload.leader_id
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    if result == "not_leader":
        raise HTTPException(status_code=403, detail="Only leader can activate")

    if result == "invalid_state":
        raise HTTPException(status_code=400, detail="Trip already active")

    return {"message": "Trip activated"}

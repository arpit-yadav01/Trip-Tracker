from fastapi import APIRouter, HTTPException
from app.schemas.user import (
    SendOTPRequest,
    VerifyOTPRequest,
    SetPasswordRequest,
    LoginRequest,
    TokenResponse
)
from app.services.user_service import (
    send_otp_service,
    verify_otp_service,
    set_password_service,
    login_service
)

router = APIRouter()


@router.post("/send-otp")
async def send_otp(payload: SendOTPRequest):
    await send_otp_service(payload.phone)
    return {"message": "OTP sent"}


@router.post("/verify-otp")
async def verify_otp(payload: VerifyOTPRequest):
    success = await verify_otp_service(payload.phone, payload.otp)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return {"message": "OTP verified"}


@router.post("/set-password")
async def set_password(payload: SetPasswordRequest):
    success = await set_password_service(payload.phone, payload.password)
    if not success:
        raise HTTPException(status_code=400, detail="OTP not verified")
    return {"message": "Password set successfully"}


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    result = await login_service(payload.phone, payload.password)

    if not result:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return result

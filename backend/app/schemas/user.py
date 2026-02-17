from pydantic import BaseModel, Field

class SendOTPRequest(BaseModel):
    phone: str = Field(..., min_length=10)

class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str

class SetPasswordRequest(BaseModel):
    phone: str
    password: str = Field(..., min_length=6)

class LoginRequest(BaseModel):
    phone: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    user_id: str

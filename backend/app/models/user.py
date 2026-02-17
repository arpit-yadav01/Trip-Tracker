from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def user_model(phone: str):
    return {
        "phone": phone,
        "hashed_password": None,
        "otp": None,
        "otp_expiry": None,
        "is_verified": False,
        "created_at": datetime.utcnow()
    }

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

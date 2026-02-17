import random
from datetime import datetime, timedelta
from app.db.mongo import users_collection
from app.models.user import user_model, hash_password, verify_password
from app.core.security import create_access_token
from bson import ObjectId


async def send_otp_service(phone: str):
    otp = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=5)

    user = await users_collection.find_one({"phone": phone})

    if not user:
        new_user = user_model(phone)
        new_user["otp"] = otp
        new_user["otp_expiry"] = expiry
        await users_collection.insert_one(new_user)
    else:
        await users_collection.update_one(
            {"phone": phone},
            {"$set": {"otp": otp, "otp_expiry": expiry}}
        )

    print(f"OTP for {phone}: {otp}")  # simulate SMS
    return True


async def verify_otp_service(phone: str, otp: str):
    user = await users_collection.find_one({"phone": phone})

    if not user:
        return False

    if user["otp"] != otp:
        return False

    if datetime.utcnow() > user["otp_expiry"]:
        return False

    await users_collection.update_one(
        {"phone": phone},
        {"$set": {"is_verified": True}, "$unset": {"otp": "", "otp_expiry": ""}}
    )

    return True


async def set_password_service(phone: str, password: str):
    hashed = hash_password(password)

    await users_collection.update_one(
        {"phone": phone},
        {"$set": {"hashed_password": hashed}}
    )

    return True


async def login_service(phone: str, password: str):
    user = await users_collection.find_one({"phone": phone})

    if not user:
        return None

    if not user["hashed_password"]:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    token = create_access_token({"sub": str(user["_id"])})

    return {
        "access_token": token,
        "user_id": str(user["_id"])
    }

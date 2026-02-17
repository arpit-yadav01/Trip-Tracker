from fastapi import FastAPI
from app.api import auth, trips

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(trips.router, prefix="/trips")

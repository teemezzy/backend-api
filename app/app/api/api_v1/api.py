from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    identity,
    user,
    login
)

api_router = APIRouter()

api_router.include_router(identity.router, prefix="/identity", tags=["identity"])
api_router.include_router(user.router, prefix="/user",tags=["user"])
api_router.include_router(login.router, prefix="/login",tags=["login"])

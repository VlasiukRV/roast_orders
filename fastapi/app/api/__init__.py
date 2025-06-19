from fastapi import APIRouter
from .http_app import router as app_router
from .http_auth import router as auth_router
from .http_users import router as users_router

api_router = APIRouter()

api_router.include_router(app_router, prefix="", tags=["api"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])

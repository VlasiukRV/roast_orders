from fastapi import APIRouter, HTTPException, Depends, status
from jose import jwt, JWTError

from app.services.fake_db import fake_users_db
from app.api.http_auth_dependencies import get_password_hash, SECRET_KEY, ALGORITHM
from app.api.http_users_dependencies import get_current_user

from app.models.user.user_schema import UserCreate

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = get_password_hash(user.password)
    fake_users_db[user.username] = {"username": user.username, "hashed_password": hashed, "refresh_token": None}
    return {"msg": "Registered"}

@router.get("/me")
def read_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"]}
from fastapi import APIRouter, HTTPException, Depends

from app.services.fake_db import fake_users_db, save_users
from app.api.auth_dependencies import get_password_hash
from app.api.users_dependencies import get_current_user

from app.models.user.user_schema import UserCreate

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = get_password_hash(user.password)
    fake_users_db[user.username] = {"username": user.username, "hashed_password": hashed, "refresh_token": None}
    save_users(fake_users_db)

    return {"msg": "Registered"}

@router.get("/me")
def read_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"]}
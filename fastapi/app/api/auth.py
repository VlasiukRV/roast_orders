
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError


from app.services.fake_db import fake_users_db, save_users
from app.api.auth_dependencies import verify_password, create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM

router = APIRouter()

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    print("User in DB:", user)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token_value = create_refresh_token(data={"sub": user["username"]})
    fake_users_db[user["username"]]["refresh_token"] = refresh_token_value
    save_users(fake_users_db)

    return {"access_token": access_token, "refresh_token": refresh_token_value, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token(refresh_token_input: str):
    try:
        payload = jwt.decode(refresh_token_input, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = fake_users_db.get(username)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user or user["refresh_token"] != refresh_token_input:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token(data={"sub": username})
    return {"access_token": new_access_token, "token_type": "bearer"}
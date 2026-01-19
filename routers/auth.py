from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from schemas.auth import TokenOut
from schemas.user import UserCreate, UserOut, LoginInsert
from utils.auth import verify_password, create_access_token, hash_password
from utils.data import read_json, write_json, next_id

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# 회원 로그인 (DONE!)
@router.post("/login",response_model=TokenOut)
def login(payload : LoginInsert):
    if payload is None:
        raise HTTPException(status_code=400, detail="Invalid form")
    users = read_json("users.json", default=[])
    user = next((u for u in users if u['email'] == payload.email), None)
    if user is None:
        raise HTTPException(status_code=400, detail="plz sign up")
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    print(f"나는 바보 {user['email']}, {user['nickname']}")
    auth = {
        "access_token": create_access_token(user["email"]),
        "token_type": "bearer",
        "expires_in": 3600
    }
    return auth

# 회원 가입 (DONE!)
@router.post("/signup",response_model=UserOut)
def signup(payload: UserCreate):
    users = read_json("users.json", default=[])
    if users is None:
        users = []
    if any(user["email"] == payload.email for user in users):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = {
        "id": next_id(users),
        "email": payload.email,
        "nickname": payload.nickname,
        "hashed_password": hash_password(payload.password),
        "created_at": datetime.now().isoformat()
    }
    users.append(user)
    write_json("users.json", users)
    return user


from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from schemas.auth import TokenOut
from schemas.user import UserCreate, UserOut
from utils.auth import verify_password, create_access_token, hash_password
from utils.data import read_json, write_json, next_id

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# 회원 로그인
@router.post("/login",response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends()):
    if form is None:
        raise HTTPException(status_code=400, detail="Invalid form")

    users = read_json("users.json", default=[])
    user = next((u for u in users if u["email"] == form.username), None)
    if not user or not verify_password(form.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(subject=str(user["email"]))
    return {"access_token": token, "token_type": "bearer"}

# 회원 가입
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


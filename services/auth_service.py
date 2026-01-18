import uuid
from datetime import datetime
from models.user import UserInternal
from repositories.user_repo import get_users, save_users
from services.jwt_service import create_access_token
from models.auth import UserSignUp, UserLogin
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password : str):
    return pwd_context.hash(password[:72])

def verify_password(plain_password : str, hashed_password :str):
    return pwd_context.verify(plain_password[:72], hashed_password)

def signup_user(data: UserSignUp):
    users = get_users()

    if any(u["email"] == data.email for u in users):
        raise HTTPException(400, "이미 존재하는 이메일")

    hashed_password = get_password_hash(data.password)
    user_creat_at = datetime.now()

    print(hashed_password)

    user = UserInternal(
        user_id= str(uuid.uuid4()),
        email= data.email,
        password = hashed_password,
        nickname =data.nickname,
        profile_image_url = data.profile_image_url,
        created_at = user_creat_at
    ).model_dump(mode="json")

    users.append(user)
    save_users(users)

    return user, *create_access_token(user["user_id"])

def login_user(data: UserLogin):
    users = get_users()
    user = next((u for u in users if u["email"] == data.username), None)

    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(401, "인증 실패")

    return user, *create_access_token(user["user_id"])

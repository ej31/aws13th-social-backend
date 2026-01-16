import uuid
from datetime import datetime, timezone

from models.user import UserInternal
from repositories.user_repo import get_users, save_users
from services.jwt_service import create_access_token
from models.auth import UserSignUp, UserLogin
from fastapi import HTTPException


def signup_user(data: UserSignUp):
    users = get_users()

    if any(u["email"] == data.email for u in users):
        raise HTTPException(400, "이미 존재하는 이메일")

    user = UserInternal(
        user_id= str(uuid.uuid4()),
        email= data.email,
        password = data.password,
        nickname =data.nickname,
        profile_image_url = data.profile_image_url,
        created_at = datetime.now(timezone.utc).isoformat(),
    ).model_dump(mode="json")

    users.append(user)

    save_users(users)

    return user, *create_access_token(user["user_id"])


def login_user(data: UserLogin):
    users = get_users()
    user = next((u for u in users if u["email"] == data.username), None)

    if not user or user["password"] != data.password:
        raise HTTPException(401, "인증 실패")

    return user, *create_access_token(user["user_id"])
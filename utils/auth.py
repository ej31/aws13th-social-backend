import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from schemas.user import TokenData
from utils import data as data_utils

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

security = HTTPBearer()

def hash_password(password: str) -> str:

    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:

    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 검증(이메일,유저아이디 없는 값 존재)",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenData(email=email, user_id=user_id)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 검증",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:

    token = credentials.credentials

    token_data = verify_token(token)

    user = data_utils.find_by_id("users.json", token_data.user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_response = {k: v for k, v in user.items() if k != "hashed_password"}

    return user_response


def create_refresh_token(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    refresh_tokens = data_utils.load_data("refresh_tokens.json")

    refresh_tokens = [rt for rt in refresh_tokens if rt.get("user_id") != user_id]

    token_id = data_utils.get_next_id("refresh_tokens.json")
    new_token = {
        "id": token_id,
        "user_id": user_id,
        "token": token,
        "expires_at": expires_at.isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    refresh_tokens.append(new_token)
    data_utils.save_data(refresh_tokens, "refresh_tokens.json")

    return token


def verify_refresh_token(token: str) -> dict:
    refresh_tokens = data_utils.load_data("refresh_tokens.json")

    token_data = next((rt for rt in refresh_tokens if rt.get("token") == token), None)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 리프레시 토큰"
        )

    expires_at = datetime.fromisoformat(token_data["expires_at"])
    if datetime.now(timezone.utc) > expires_at:
        delete_refresh_token(token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="만료된 리프레시 토큰"
        )

    return token_data


def delete_refresh_token(token: str) -> bool:
    refresh_tokens = data_utils.load_data("refresh_tokens.json")
    original_length = len(refresh_tokens)

    refresh_tokens = [rt for rt in refresh_tokens if rt.get("token") != token]

    if len(refresh_tokens) < original_length:
        return data_utils.save_data(refresh_tokens, "refresh_tokens.json")
    return False


def delete_user_refresh_tokens(user_id: int) -> bool:
    refresh_tokens = data_utils.load_data("refresh_tokens.json")
    refresh_tokens = [rt for rt in refresh_tokens if rt.get("user_id") != user_id]
    return data_utils.save_data(refresh_tokens, "refresh_tokens.json")

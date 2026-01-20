from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette.requests import Request
from typing import Optional
from core.config import jwt_settings
from repositories.user_repo import get_users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            jwt_settings.SECRET_KEY,
            algorithms=[jwt_settings.ALGORITHM],
        )
    except JWTError as err:
        raise HTTPException(status_code=401, detail="토큰 오류") from err

    user_id = payload.get("sub")
    user = next((u for u in get_users() if u["user_id"] == user_id), None)

    if not user:
        raise HTTPException(status_code=401, detail="유저 없음")

    return user


def get_optional_user(request: Request) -> Optional[dict]:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            jwt_settings.SECRET_KEY,
            algorithms=[jwt_settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import os
import secrets

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 설정
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY 환경변수가 설정되지 않았습니다. 프로덕션 배포 전 반드시 설정하세요.")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

def hash_password(password: str) -> str:
    """비밀번호를 해싱합니다."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호를 검증합니다."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    JWT 액세스 토큰을 생성합니다.

    Args:
        data: 토큰에 담을 데이터
        expires_delta: 만료 시간

    Returns:
        JWT 토큰 문자열
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    JWT 토큰을 검증하고 페이로드를 반환합니다.

    Args:
        token: JWT 토큰 문자열

    Returns:
        토큰에 담긴 데이터 또는 None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user_id(token: str) -> int | None:
    """토큰에서 현재 사용자 ID를 추출합니다."""
    payload = verify_token(token)
    if payload:
        return payload.get("userId")
    return None

def create_refresh_token(user_id: int) -> dict:
    """
    리프레시 토큰을 생성합니다.
    유효기간: 7일
    """
    token = secrets.token_urlsafe(32)
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    return {
        "token": token,
        "userId": user_id,
        "expiresAt": expire.isoformat()
    }

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    JWT 토큰을 검증하고 현재 사용자 정보를 반환합니다.
    """
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "code": "UNAUTHORIZED",
                "message": "유효하지 않은 토큰입니다."
            }
        )

    return payload


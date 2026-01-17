
# 인증/인가 유틸 + Depends 제공
# 1. 비밀번호 해시/검증
# 2. 토큰(JWT) 발급/검증
# (현재 구현은 알할거지만)
# 권한 체크 헬퍼 (Require_admin, require_owner)

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from utils.data import read_json


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM" , "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
# os.getenv(a,b) .env or 환경변수에 a 이름 있으면 앞에꺼 없으면 뒤에꺼(기본값)
# 그리고 os.getenv 쓰려면 환경변수 등록하거나 .env 파일에 정의해두고 main 에서 앱 실행 후 load_dotenv() 한번만 해주면 됨.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
# oauth2 인증 스킴/ Bearer<token> 형식, users/login에서 발급받는다

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(subject: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id # 토큰 발급 주체 반환
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired") # 나중에 예외처리 세분화 하기

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    user_id = decode_token(token)
    users = read_json("users.json", default=[])
    user = next((u for u in users if str(u["id"]) == str(user_id)),None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
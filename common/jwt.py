from fastapi import HTTPException,status
from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError

from common.config import settings
from datetime import datetime, timezone, timedelta

#access Token 생성
def create_access_token(subject:str) -> str:
    minutes = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_minutes = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode = {"exp": expire_minutes,
                 "sub":str(subject)}

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(subject: str) -> str:
    days = int(settings.REFRESH_TOKEN_EXPIRE_DAYS)
    expire_minutes = datetime.now(timezone.utc) + timedelta(minutes=days)

    to_encode = {"exp":expire_minutes,"sub":str(subject),"type":"refresh"}

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        email: str= payload.get("sub")

        if not email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="사용자 정보가 없습니다.")

        if payload.get("type") == "refresh":
            return None

        return email

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="토큰이 만료되었습니다.")
    except JWTClaimsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="토큰의 클레임 정보가 유효하지 않습니다.")
    except JWTError:
        #서명 오류, 형식 오류 등 모든 나머지를 여기서 처리한다.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="유효하지 않은 토큰입니다.")
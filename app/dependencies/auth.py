from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.utils.jwt import decode_token
from app.utils.data import read_users

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    JWT 토큰을 검증하고,
    users.json에서 해당 사용자를 찾아 반환하는 함수
    """

    # 1️⃣ Authorization 헤더 자체가 없는 경우
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다."
        )

    # 2️⃣ Bearer 타입이 아닌 경우
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 인증 방식입니다."
        )

    # 3️⃣ JWT 토큰 문자열 추출
    token = credentials.credentials

    # 4️⃣ 토큰 검증 + payload에서 sub 추출
    try:
        # decode_token은 sub(email)를 반환하도록 구현돼 있음
        email = decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 유효하지 않습니다."
        )

    # 5️⃣ users.json에서 해당 사용자 찾기
    users = read_users()
    user = next((u for u in users if u.get("email") == email), None)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다."
        )

    # 6️⃣ 인증 성공 → 사용자 dict 반환
    return user

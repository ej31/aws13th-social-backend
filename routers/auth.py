from fastapi import APIRouter, HTTPException, status, Body
from typing import Annotated
from schemas import auth
from utils.data import load_data
from utils.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", status_code=status.HTTP_200_OK)
async def auth_token(
        login_data: Annotated[auth.LoginRequest, Body()]
):
    # 전체 사용자 목록 로드
    users = load_data("users.json")

    # 이메일 일치하는 사용자 찾기

    user = next((u for u in users if u['email'] == login_data.email), None)

    # 계정이 없거나 비밀번호가 틀린경우 에러 발생
    if not user or not verify_password(login_data.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "error",
                "message": "이메일 또는 비밀번호가 틀렸습니다."
            }
        )

    # 사용자 식별정보(email)를 담은 진짜 JWT 토큰 생성
    access_token = create_access_token(data={"sub": user['email']})
    return {
        "status": "success",
        "data": {
            "token_type": "Bearer",
            "access_token": access_token,
            "expires_in": 3600
        }
    }
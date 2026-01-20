"""
인증 API
- 로그인
"""
from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import LoginRequest, LoginResponse, LoginUserInfo
from app.schemas.common import APIResponse
from app.core.security import verify_password, create_access_token
from app.core.config import get_settings
from app.api.deps import UserRepo

router = APIRouter()
settings = get_settings()


@router.post("/tokens", response_model=APIResponse[LoginResponse])  # 경로 변경
def login(
    credentials: LoginRequest,
    user_repo: UserRepo
):
    """
    로그인
    """
    # 사용자 조회
    user = user_repo.find_by_email(credentials.email)
    
    # 사용자가 없거나 비밀번호가 일치하지 않으면 에러
    if user is None or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 일치하지 않습니다"
        )
    
    # JWT 토큰 생성
    access_token = create_access_token(
        data={
            "sub": user["email"],
            "user_id": user["user_id"]
        }
    )
    
    # 응답 데이터 구성
    login_response = LoginResponse(
        access_token=access_token,
        token_type="Bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # 초 단위
        user=LoginUserInfo(
            user_id=user["user_id"],
            email=user["email"],
            nickname=user["nickname"]
        )
    )
    
    return APIResponse(
        status="success",
        data=login_response
    )
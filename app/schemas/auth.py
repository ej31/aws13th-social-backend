"""
인증 관련 스키마
"""
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    """
    로그인 요청 (POST /auth/tokens)

    Attributes:
        email: 이메일 주소
        password: 비밀번호
    """
    email: str = Field(description="이메일 주소")
    password: str = Field(description="비밀번호")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "password123"
                }
            ]
        }
    }

class LoginUserInfo(BaseModel):
    """
    로그인 응답에 포함되는 사용자 정보

    Attributes:
        user_id: 사용자 ID
        email: 이메일 주소
        nickname: 닉네임
    """
    user_id: int = Field(description="사용자 ID")
    email: str = Field(description="이메일 주소")
    nickname: str = Field(description="닉네임")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 123,
                    "email": "user@example.com",
                    "nickname": "클라우드유저"
                }
            ]
        }
    }

class LoginResponse(BaseModel):
    """
    로그인 응답

    Attributes:
        access_token: JWT 액세스 토큰
        token_type: 토큰 타입 (Bearer)
        expires_in: 토큰 만료 시간 (초)
        user: 사용자 정보
    """
    access_token: str = Field(description="JWT 액세스 토큰")
    token_type: str = Field(default="Bearer", description="토큰 타입")
    expires_in: int = Field(description="토큰 만료 시간 (초)")
    user: LoginUserInfo = Field(description="사용자 정보")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "Bearer",
                    "expires_in": 3600,
                    "user": {
                        "user_id": 123,
                        "email": "user@example.com",
                        "nickname": "클라우드유저"
                    }
                }
            ]
        }
    }
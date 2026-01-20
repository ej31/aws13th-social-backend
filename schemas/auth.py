from pydantic import BaseModel, EmailStr, Field, field_validator
from .common import validate_password_logic


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="가입한 이메일", examples=["example@naver.com"])
    password: str = Field(..., description="비밀번호(8자 이상, 영문/숫자/특수문자 포함)")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        # 이전에 정의한 공통 로직을 사용하여 의존성 분리 및 일관성 유지
        return validate_password_logic(v)

class TokenData(BaseModel):
    token_type: str = Field("Bearer",description="토큰 타입")
    access_token: str = Field(...,description="실제 API에서 사용되는 토큰")
    expires_in: int = Field(3600, description="토큰 만료 시간(초)")

class LoginResponse(BaseModel):
    status: str ="success"
    data: TokenData

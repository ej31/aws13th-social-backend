from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# 공통 응답 구조를 위한 베이스 모델
class ResponseBase(BaseModel):
    status: str = "success"

# 회원가입 요청 규격
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="8자 이상의 비밀번호")
    nickname: str = Field(..., min_length=2, description="2자 이상의 닉네임")
    profile_image_url: Optional[str] = None

# 회원 정보 응답 규격
class UserInfo(BaseModel):
    id: str
    email: EmailStr
    nickname: str
    profile_image_url: Optional[str]
    created_at: datetime

# 최종 회원가입 응답 구조
class UserRegistrationResponse(ResponseBase):
    data: UserInfo
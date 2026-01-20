from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime

# 회원가입
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    profile_image: Optional[HttpUrl] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    profile_image: Optional[HttpUrl] = None
    password: Optional[str] = None

# 회원 탈퇴
class UserDelete(BaseModel):
    password: str

# 사용자 응답
class UserResponse(BaseModel):
    email: EmailStr
    id: int  # 또는 str (DB 타입에 따라)
    nickname: str
    profile_image: Optional[HttpUrl] = None
    created_at: datetime
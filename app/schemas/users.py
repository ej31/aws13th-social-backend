# schemas/users.py
from pydantic import BaseModel,Field,field_validator
from datetime import datetime
import re


class Pagination(BaseModel):
    page: int
    limit: int
    total: int


# ===== Requests =====
class UserSignupRequest(BaseModel):
    email: str
    password: str = Field(min_length= 2, max_length=20)
    nickname: str
    profile_image: str | None = None

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if not re.search(r"\d", v) and not re.search(r"[^\w\s]", v):
            raise ValueError("비밀번호에는 숫자와 특수문자가 반드시 포함되어야 합니다.")
        if not re.search(r"\d", v):
            raise ValueError("비밀번호에는 숫자가 반드시 포함되어야 합니다.")
        if not re.search(r"[^\w\s]", v):
            raise ValueError("비밀번호에는 특수문자가 반드시 포함되어야 합니다.")
        return v



class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserProfileUpdateRequest(BaseModel):
    new_nickname: str | None = None
    new_profile_image: str | None = None
    new_password: str | None = None
    current_password: str | None = None  # 문서상 X지만 예시/설명에 존재 :contentReference[oaicite:3]{index=3}


# ===== Responses: Users =====
class UserSignupData(BaseModel):
    id: int
    email: str
    nickname: str
    profile_image: str | None = None
    created_at: datetime


class UserSignupResponse(BaseModel):
    status: str
    data: UserSignupData


class PublicUserProfile(BaseModel):
    id: int
    nickname: str
    profile_image: str
    created_at: datetime


class PublicUserProfileResponse(BaseModel):
    status: str
    data: PublicUserProfile


class MyProfile(BaseModel):
    # 문서에 id가 이메일로 내려옴 :contentReference[oaicite:4]{index=4}
    id: str
    nickname: str
    profile_image: str
    created_at: datetime


class MyProfileResponse(BaseModel):
    status: str
    data: MyProfile


class UserProfileUpdateData(BaseModel):
    nickname: str
    profile_image: str


class UserProfileUpdateResponse(BaseModel):
    status: str
    message: str
    data: UserProfileUpdateData


# ===== Responses: Auth(Token) =====
class TokenData(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenCreateResponse(BaseModel):
    status: str
    data: TokenData


# ===== Fail Response (공통) =====
class FailResponse(BaseModel):
    status: str
    message: str

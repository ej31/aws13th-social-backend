from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    profile_img: str | None = None


class UserCreateResponse(BaseModel):
    id: int
    nickname: str
    created_at: datetime


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str


class UserMyProfile(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    profile_img: str | None = None
    created_at: datetime


class UserUpdateRequest(BaseModel):
    nickname: str | None = None
    profile_img: str | None = None


class UserProfile(BaseModel):
    id: int
    nickname: str
    profile_img: str | None = None


from datetime import datetime

from pydantic import BaseModel, EmailStr, model_validator


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    profile_img: str | None = None


class UserCreateResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    nickname: str
    created_at: datetime


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    model_config = {"from_attributes": True}

    access_token: str


class UserMyProfile(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    email: EmailStr
    nickname: str
    profile_img: str | None = None
    created_at: datetime


class UserUpdateRequest(BaseModel):
    nickname: str | None = None
    profile_img: str | None = None

    @model_validator(mode='after')
    def check_at_least_one_field(self):
        if self.nickname is None and self.profile_img is None:
            raise AttributeError("최소 하나의 필드는 입력해야 합니다")
        return self


class UserProfile(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    nickname: str
    profile_img: str | None = None


from datetime import datetime
import re

from pydantic import BaseModel, EmailStr, model_validator, StringConstraints, AfterValidator
from typing import Annotated

SPECIAL_CHARS = r"!\"#$%&'()*+,\-./:;<=>?@\[₩\]\^_`{|}~"


def validate_password(v: str) -> str:
    if not re.search(r"[A-Z]", v):
        raise ValueError("비밀번호에 대문자가 포함되어야 합니다")
    if not re.search(r"[a-z]", v):
        raise ValueError("비밀번호에 소문자가 포함되어야 합니다")
    if not re.search(r"\d", v):
        raise ValueError("비밀번호에 숫자가 포함되어야 합니다")
    if not re.search(rf"[{SPECIAL_CHARS}]", v):
        raise ValueError("비밀번호에 특수문자가 포함되어야 합니다")
    return v


Password = Annotated[
    str,
    StringConstraints(
        min_length=8,
        max_length=16,
    ),
    AfterValidator(validate_password),
]

Nickname = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=10,
        pattern=r"^[A-Za-z0-9]+$",
    ),
]


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: Password
    nickname: Nickname
    profile_img: str | None = None


class UserCreateResponse(BaseModel):
    id: int
    nickname: Nickname
    email: EmailStr
    created_at: datetime


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str


class UserMyProfile(BaseModel):
    id: int
    email: EmailStr
    nickname: Nickname
    profile_img: str | None = None
    created_at: datetime


class UserUpdateRequest(BaseModel):
    nickname: Nickname | None = None
    profile_img: str | None = None

    @model_validator(mode='after')
    def check_at_least_one_field(self):
        if self.nickname is None and self.profile_img is None:
            raise ValueError("최소 하나의 필드는 입력 해야 합니다")
        return self


class UserProfile(BaseModel):
    id: int
    nickname: Nickname
    profile_img: str | None = None


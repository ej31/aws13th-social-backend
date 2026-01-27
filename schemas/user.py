import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, ConfigDict, field_serializer
from common.security import encode_id


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일 (중복 불가)")
    nickname: str = Field(
        ...,
        min_length=2,
        max_length=20,
        pattern=r"^[가-힣a-zA-Z0-9]+$",
        description="닉네임 (2~20자, 특수문자 불가)"
    )
    profile_image: Optional[str] = Field(None, description="프로필 이미지 URL 또는 경로")


class SignupRequest(UserBase):
    password: str = Field(..., min_length=8, max_length=20, description="비밀번호 (영문/숫자 포함)")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Za-z]", v) or not re.search(r"[0-9]", v):
            raise ValueError("비밀번호는 영문자와 숫자를 모두 포함해야 합니다.")
        return v


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, min_length=2, max_length=20, pattern=r"^[가-힣a-zA-Z0-9]+$", description="닉네임")
    password: Optional[str] = Field(None, min_length=8, max_length=20, description="새 비밀번호")
    current_password: str = Field(..., description="본인 확인용 현재 비밀번호")  # 수정 시 필수 권장

    @field_validator("password")
    @classmethod
    def validate_new_password(cls, v: Optional[str]):
        if v is None:
            return v
        if not re.search(r"[a-zA-Z]", v) or not re.search(r"\d", v):
            raise ValueError("새 비밀번호는 영문자와 숫자를 포함해야 합니다.")
        return v


class UserResponse(UserBase):
    id: str
    created_at: datetime  # ISO 문자열이 아닌 실제 datetime 객체

    # SQLAlchemy 객체를 Pydantic으로 변환하기 위한 설정
    model_config = ConfigDict(from_attributes=True)

    # 클라이언트에게 나갈 때만 ID를 HashID로 인코딩
    @field_serializer("id")
    def serialize_id(self, v: int) -> str:
        return encode_id(v)


class UserSearchResponse(BaseModel):
    nickname: str
    profile_image: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"
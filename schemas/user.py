import re
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일 (중복 불가)")
    nickname: str = Field(
        ...,
        min_length=2,
        max_length=20,
        pattern=r"^[가-힣a-zA-Z0-9]+$",
        description="닉네임 (2~20자, 특수문자 불가)"
    )
    profile_image: str | None = Field(None, description="프로필 이미지 URL 또는 경로")

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
    nickname: Optional[str] = Field(None, min_length=2, max_length=20, pattern=r"^[가-힣a-zA-Z0-9]+$",description="닉네임 (2~20자, 특수문자 불가)")
    password: Optional[str] = Field(None, min_length=8, max_length=20, description="새 비밀번호")
    current_password: str = Field(..., min_length=8, max_length=20, description="기존 비밀번호 (본인 인증용)")

    @field_validator("password")
    @classmethod
    def validate_new_password(cls, v: Optional[str]):
        if v is None: return v
        if not re.search(r"[a-zA-Z]", v) or not re.search(r"\d", v):
            raise ValueError("새 비밀번호는 영문자와 숫자를 포함해야 합니다.")
        return v

    @model_validator(mode="after")
    def check_password_update_requirements(self) -> 'UserUpdateRequest':
        if self.password and not self.current_password:
            raise ValueError("비밀번호를 변경하려면 현재 비밀번호 입력이 필수입니다.")
        return self

class UserInternal(UserBase):
    id: int  # DB 내 PK (int)
    password: str  # 해싱된 비밀번호 저장
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: Optional[str] = None

class UserResponse(UserBase):
    created_at: datetime

class UserSearchResponse(BaseModel):
    nickname: str
    profile_image: Optional[str]

class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"
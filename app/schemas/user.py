"""
사용자 관련 스키마
"""
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from ..utils.validators import (
    validate_email_format,
    validate_password_strength,
    validate_nickname_length
)

class UserSignupRequest(BaseModel):
    """
    회원가입 요청

    Attributes:
        email: 이메일 주소
        password: 비밀번호 (최소 8자, 영문/숫자 조합)
        nickname: 닉네임 (2~20자)
        profile_image: 프로필 이미지 URL (선택)
    """
    email: str = Field(description="이메일 주소")
    password: str = Field(min_length=8, description="비밀번호")
    nickname: str = Field(min_length=2, max_length=20, description="닉네임")
    profile_image: str | None = Field(default=None, description="프로필 이미지 URL")

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        return validate_email_format(v)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_strength(v)

    @field_validator('nickname')
    @classmethod
    def validate_nickname(cls, v: str) -> str:
        return validate_nickname_length(v)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "password123",
                    "nickname": "클라우드유저",
                    "profile_image": "https://example.com/profile.jpg"
                }
            ]
        }
    }

class UserUpdateRequest(BaseModel):
    """
    프로필 수정 요청

    Attributes:
        nickname: 변경할 닉네임 (선택)
        profile_image: 변경할 프로필 이미지 URL (선택)
        password: 변경할 비밀번호 (선택)
    """
    nickname: str | None = Field(default=None, min_length=2, max_length=20, description="닉네임")
    profile_image: str | None = None
    password: str | None = Field(default=None, min_length=8, description="비밀번호")

    @field_validator('nickname')
    @classmethod
    def validate_nickname(cls, v: str | None) -> str | None:
        if v is not None:
            return validate_nickname_length(v)
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str | None) -> str | None:
        if v is not None:
            return validate_password_strength(v)
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nickname": "새로운닉네임",
                    "profile_image": "https://example.com/new-profile.jpg"
                }
            ]
        }
    }

class UserProfileResponse(BaseModel):
    """
    사용자 프로필 응답 (본인)

    Attributes:
        user_id: 사용자 ID
        email: 이메일 주소
        nickname: 닉네임
        profile_image: 프로필 이미지 URL
        created_at: 생성일시
        updated_at: 수정일시
    """
    user_id: int = Field(description="사용자 ID")
    email: str = Field(description="이메일 주소")
    nickname: str = Field(description="닉네임")
    profile_image: str = Field(description="프로필 이미지 URL")
    created_at: datetime = Field(description="생성일시")
    updated_at: datetime = Field(description="수정일시")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 123,
                    "email": "user@example.com",
                    "nickname": "클라우드유저",
                    "profile_image": "https://example.com/profile.jpg",
                    "created_at": "2026-01-06T10:00:00Z",
                    "updated_at": "2026-01-06T10:00:00Z"
                }
            ]
        }
    }

class UserPublicResponse(BaseModel):
    """
    사용자 공개 프로필 응답 (타인)

    Attributes:
        user_id: 사용자 ID
        nickname: 닉네임
        profile_image: 프로필 이미지 URL
        created_at: 생성일시
    """
    user_id: int = Field(description="사용자 ID")
    nickname: str = Field(description="닉네임")
    profile_image: str = Field(description="프로필 이미지 URL")
    created_at: datetime = Field(description="생성일시")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 123,
                    "nickname": "클라우드유저",
                    "profile_image": "https://example.com/profile.jpg",
                    "created_at": "2026-01-06T10:00:00Z"
                }
            ]
        }
    }

class UserAuthorInfo(BaseModel):
    """
    작성자 정보 (게시글/댓글에 포함)

    Attributes:
        user_id: 사용자 ID
        nickname: 닉네임
        profile_image: 프로필 이미지 URL
    """
    user_id: int = Field(description="사용자 ID")
    nickname: str = Field(description="닉네임")
    profile_image: str = Field(description="프로필 이미지 URL")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 123,
                    "nickname": "클라우드유저",
                    "profile_image": "https://example.com/profile.jpg"
                }
            ]
        }
    }
    
    
    """
    field_vaildator의 기본값 mode='after'
    pydantic의 기본 타입 변환 후에 validator 실행
    ex) str 타입 검증 -> 문자열로 변환됨 -> 그 다음 validator 실행
    """
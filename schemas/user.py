from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime


# (POST /users)
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="비밀번호는 8자 이상")
    nickname: str = Field(..., min_length=2, max_length=20)
    profile_image: Optional[str] = None

# (POST /auth/tokens)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# (PATCH /users/me)
class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, min_length=2, max_length=20)
    profile_image: Optional[str] = None

    # 비밀번호 변경
    current_password: Optional[str] = Field(None, description="본인 확인용 기존 비밀번호")
    new_password: Optional[str] = Field(None, min_length=8, description="새 비밀번호")
    new_password_confirm: Optional[str] = Field(None, min_length=8, description="새 비밀번호 확인")

    # 비밀번호 검증
    @model_validator(mode='after')
    def check_passwords_match(self):
        pw1 = self.new_password
        pw2 = self.new_password_confirm

        # 새 비밀번호 검증
        if pw1 is not None and pw1 != pw2:
            raise ValueError('새 비밀번호와 비밀번호 확인이 일치하지 않습니다.')
        return self

# (DELETE /users/me)
class UserDelete(BaseModel):
    password: str

# (GET /users/me)
class UserMeResponse(BaseModel):
    id: int
    email: str
    nickname: str
    profile_image: Optional[str] = None
    created_at: datetime

# (GET /users/{user_id})
class UserPublicResponse(BaseModel):
    id: int
    nickname: str
    profile_image: Optional[str] = None
    created_at: datetime
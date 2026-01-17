from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime


class UserInternal(BaseModel):
    user_id: str
    email: EmailStr
    password: str
    nickname: Optional[str]
    profile_image_url: Optional[HttpUrl]
    created_at: datetime

class UserPublic(BaseModel):
    email: EmailStr
    nickname: Optional[str]
    profile_image_url: Optional[HttpUrl]


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserPublic
    issued_at: datetime


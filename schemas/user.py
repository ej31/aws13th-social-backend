from datetime import datetime

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    profile_image_url: str | None = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    profile_image_url: str | None = None
    created_at: datetime

class LoginInsert(BaseModel):
    email: EmailStr
    password: str

class NickNameUpdateIn(BaseModel):
    nickname: str

class PasswordChangeIn(BaseModel):
    new_password: str
    old_password: str
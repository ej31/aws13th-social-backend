from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str
    nickname: str
    profileImage: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    userId: int
    email: str
    nickname: str
    profileImage: str | None = None
    createdAt: datetime

class UserPublicResponse(BaseModel):
    userId: int
    nickname: str
    profileImage: str | None = None
    createdAt: datetime

class UserUpdate(BaseModel):
    nickname: str | None = None
    profileImage: str | None = None
    password: str | None = None
    currentPassword: str | None = None

class UserDelete(BaseModel):
    password: str

class LoginResponse(BaseModel):
    userId: int
    nickname: str
    accessToken: str
    tokenType: str = "Bearer"
    expiresIn: int
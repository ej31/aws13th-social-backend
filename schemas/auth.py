
from pydantic import BaseModel

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    username: str | None = None


# class UserOut(BaseModel):
#     id: int
#     email: EmailStr
#     nickname: str
#     created_at: datetime
#
# class UserCreate(BaseModel):
#     email: EmailStr
#     nickname: str

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str
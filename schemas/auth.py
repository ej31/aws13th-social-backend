from datetime import datetime
from pydantic import BaseModel, EmailStr

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

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
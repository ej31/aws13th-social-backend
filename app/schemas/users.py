from pydantic import BaseModel
class User(BaseModel):
    email: str
    password: str
    nickname: str
    profile_image: str

class UserSignupRequest(BaseModel):
    email: str
    password: str
    nickname: str
    profile_image: str | None = None

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserUpdateRequest(BaseModel):
    current_password: str
    new_nickname: str
    new_password: str
    new_profile_image: str | None = None
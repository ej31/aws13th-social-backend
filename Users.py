from datetime import datetime
from typing import Annotated, Optional
from fastapi import FastAPI, UploadFile, Body
from pydantic import BaseModel, Field, HttpUrl
from starlette import status
from pydantic import EmailStr
from starlette.exceptions import HTTPException

app = FastAPI()

class UsersForm :
    email: Annotated[EmailStr, Form()],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    password_confirm: Annotated[str, Form()],
    # 파일 업로드 (프로필 이미지)
    profile_image: Annotated[UploadFile, File()] = None

class UsersBase(BaseModel):
    nickname = Annotated[
        Optional[str], Field(min_length=2, max_length=20, description="2자 이상 20자 이하의 닉네임")] = None
    email = Annotated[EmailStr, Field(description="사용자 이메일")]
    password = Annotated[str, Field(min_length=8, max_length=50)] # 비밀번호 복잡성 로직은 나중에 추가
    profile_image_url: Optional[HttpUrl] = None

class UserResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user : UsersBase
    created_at: datetime


@app.post("/auth/signup",response_model=UserResponse)
async def signup(user: UsersBase):
    return user

@app.post("/auth/login",response_model=UserResponse)
async def login(user: UsersBase):
    return user

# @app.post("/auth/logout")
# async def logout(user: Users):
#     return {"logout": user}

@app.get("/users/me",response_model=UserResponse)
async def get_users():
    return {"username": "admin", "email": "", "password": ""}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.patch("/users/me")
async def update_user(user_id: int):
    return {"user_id": user_id}

@app.delete("/users/me")
async def delete_user(user_id: int):
    return {"user_id": user_id}

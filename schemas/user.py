from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# 응답용 사용자 데이터 모델
class UserData(BaseModel):
    id: int
    email: str
    nickname: str
    profileImage: Optional[str] = None
    createdAt: datetime

# 회원가입 성공 응답 모델
class SignupResponse(BaseModel):
    status: str
    data: UserData

# [1] 로그인 요청 (Request Body)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# [2] 로그인 응답 내부 데이터 (User 정보)
class LoginUserInfo(BaseModel):
    id: int
    email: str
    nickname: str

# [3] 로그인 응답 내부 데이터 (Token + User)
class LoginData(BaseModel):
    accessToken: str
    user: LoginUserInfo

# [4] 최종 로그인 응답 (Response Wrapper)
class LoginResponse(BaseModel):
    status: str
    data: LoginData
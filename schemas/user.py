from pydantic import BaseModel, EmailStr
from typing import Optional
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

# [1] 프로필 내부 데이터 모델
class UserProfile(BaseModel):
    id: int
    email: str
    nickname: str
    profileImage: Optional[str]
    joinedAt: str  # 명세서에는 joinedAt으로 되어있음

# [2] 전체 응답 감싸개
class ProfileResponse(BaseModel):
    status: str
    data: UserProfile


#프로필 수정 응답용 데이터 모델
class UpdatedUserProfile(BaseModel):
    id: int
    nickname: str
    profileImage: Optional[str]
    createdAt: str

class UpdateProfileResponse(BaseModel):
    status: str
    data: UpdatedUserProfile

#공개 프로필 조회용 데이터 모델 (특정 회원 조회)
class PublicUserProfile(BaseModel):
    id: int
    nickname: str
    profileImage: Optional[str]

class PublicUserResponse(BaseModel):
    status: str
    data: PublicUserProfile
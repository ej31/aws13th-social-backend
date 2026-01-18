from pydantic import BaseModel
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
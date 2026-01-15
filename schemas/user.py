import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

#공통 유저 모델
class UserBase(BaseModel):
    #...은 엘립시스 이 필드는 기본값이 없으면 반드시 데이터가 들어와야 하는 required 필드
    '''
        Field(...) : 필수 항목, 데이터가 없으면 422 에러 반환
        Field(None) : 선택 항목 데이터가 없으면 None이 들어감
        Field("기본값") : 선택 항목 데이터가 없으면, "기본값"이 들어감
        description = API 메타데이터, Swagger 설명
    '''

    email: EmailStr = Field(...,description="사용자 이메일 (중복 불가)")
    nickname: str = Field(
        ...,
        min_length=2,
        max_length=20,
        #한글,영문,숫자만 허용하고 공백이나 특수문자는 안됨
        pattern=r"^[가-힣a-zA-Z0-9]+$",
        description="닉네임 (2~20자, 특수문자 불가)"
    )

#회원가입 요청
class SignupRequest(UserBase):
    password: str = Field(...,min_length=8,max_length=20,description="비밀번호 (영문/숫자/특수문자 포함)")

    @field_validator("password") # 클래스 내부의 필드 password
    @classmethod # 아직 객체가 생성되지 않았으므로 클래스메서드 선언
    def validate_password(cls,v: str) -> str: # 반환 타입 str
        #re.search는 문자열 전체에서 해당 패턴이 하나라도 있는지 찾는다.

        #영문 대문자 또는 소문자가 하나라도 포함되는지 확인
        if not re.search(r"[A-Za-z]",v):
            raise ValueError("비밀번호에 영문자가 포함되어야 합니다.")
        #숫자 0-9가 하나라도 포함되는지 확인한다.
        if not re.search(r"[0-9]",v):
            raise ValueError("비밀번호에 숫자가 포함되어야 합니다.")

        # 버그로 인해 잠시 주석 처리
        # #비밀번호에 특수문자가 하나라도 포함되는지 확인
        # if not re.search(r"[!@#$%^&*]",v):
        #     raise ValueError("비밀번호에 특수문자가 포함되어야 합니다.")

        return v

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserUpdateRequest(BaseModel):
    nickname: str | None = Field(None,min_length=2,max_length=20,pattern=r"^[가-힣a-zA-Z0-9]+$",description="한글,영문,대소문자만 허용한다.")
    password: str | None = Field(None,min_length=8,max_length=20,description="바꾸고 싶은 비밀번호")
    current_password: str | None = Field(...,min_length=8,max_length=20,description="원래 사용하고 있던 비밀번호")

    @field_validator("password")
    def validate_password_complexity(cls, v: Optional[str]):
        # 비밀번호를 입력하지 않은 경우(None)는 검증 통과 (수정 안 함)
        if v is None:
            return v

        if not re.search(r"[a-zA-Z]", v):
            raise ValueError("비밀번호에는 최소 하나 이상의 영문자가 포함되어야 합니다.")

        if not re.search(r"\d", v):
            raise ValueError("비밀번호에는 최소 하나 이상의 숫자가 포함되어야 합니다.")
        return v

    def check_password_update_requirements(self,v):
        #새 비밀번호는 있는데 현재 비밀번호가 없는 경우
        if self.password and not self.current_password:
            raise ValueError("비밀번호를 변경하려면 현재 비밀번호를 입력해야 합니다.")
        return self

class UserResponse(UserBase):
    id: str
    email: str
    nickname: str
    profile_image: str | None
    created_at: datetime

class UserQueryResponse(UserBase):
    nickname: str
    profile_image: str | None

class UserUpdateResponse(UserBase):
    email: EmailStr
    nickname: str
    profile_image: str | None = None
    created_at: datetime

class TokenData(BaseModel):
    access_token: str
    token_type : str = "bearer"

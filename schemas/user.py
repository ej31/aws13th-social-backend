import re
from datetime import datetime
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
class UserCreate(UserBase):
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
        #비밀번호에 특수문자가 하나라도 포함되는지 확인
        if not re.search(r"[!@#$%^&*]",v):
            raise ValueError("비밀번호에 특수문자가 포함되어야 합니다.")

        return v

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class UserUpdate(BaseModel):
    nickname: str | None = Field(None,min_length=2,max_length=20,pattern=r"^[가-힣a-zA-Z0-9]+$")

class UserResponse(UserBase):
    id : str
    profileImage: str | None
    createdAt: datetime

class Token(BaseModel):
    access_token: str
    token_type : str = "bearer"


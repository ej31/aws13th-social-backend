# from typing import Optional, Annotated
# from pydantic import BaseModel, EmailStr, Field, HttpUrl, model_validator
# from fastapi import Form
#
# #class와 @classmethod 데코레이터 사용 하여 form으로 pydantic검증
# #class 안에 pydantic과 form을 한번에 끝낼수 있음
# class UserSignUp(BaseModel):
#     email: EmailStr
#     password: str = Field(min_length=8, max_length=50)
#     password_confirm: str
#     nickname: Optional[str] = Field(default=None, min_length=2, max_length=20)
#     profile_image_url: Optional[HttpUrl] = None
#
#     @model_validator(mode="after")
#     def password_match(self):
#         if self.password != self.password_confirm:
#             raise ValueError("패스워드 불일치")
#         return self
#
#     @classmethod
#     def as_form(
#         cls,
#         email: EmailStr = Form(...),
#         password: str = Form(...),
#         password_confirm: str = Form(...),
#         nickname: Optional[str] = Form(None),
#         profile_image_url: Optional[HttpUrl] = Form(None),
#     ):
#         return cls(**locals())
#
# class UserLogin(BaseModel):
#     username : EmailStr
#     password: str
#
#     @classmethod
#     def as_form(
#         cls,
#         email: EmailStr = Form(...),
#         password: str = Form(...)
#     ):
#         return cls(username =email, password=password)
#
# class UserUpdate(BaseModel):
#     # 수정하고 싶은 필드만 선택적으로 받을 수 있게 Optional 처리
#     email: Annotated[Optional[EmailStr], Field(description="사용자 이메일")] = None
#     password: Annotated[Optional[str], Field(min_length=8, max_length=50)] = None
#     nickname: Annotated[Optional[str], Field(min_length=2, max_length=20)] = None
#     profile_image_url: Optional[HttpUrl] = None
#
#     @classmethod
#     def as_form(
#         cls,
#         email: Optional[EmailStr] = Form(None),
#         nickname: Optional[str] = Form(None),
#         password: Optional[str] = Form(None),
#         profile_image_url: Optional[HttpUrl] = Form(None)
#     ):
#         return cls(**locals())
from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, Field, HttpUrl, model_validator
from fastapi import Form

# --- [1. 순수한 Pydantic 데이터 모델 정의] ---

class UserSignUp(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)
    password_confirm: str
    nickname: Optional[str] = Field(default=None, min_length=2, max_length=20)
    profile_image_url: Optional[HttpUrl] = None

    @model_validator(mode="after")
    def password_match(self):
        if self.password != self.password_confirm:
            raise ValueError("패스워드 불일치")
        return self

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(default=None, description="사용자 이메일")
    password: Optional[str] = Field(default=None, min_length=8, max_length=50)
    nickname: Optional[str] = Field(default=None, min_length=2, max_length=20)
    profile_image_url: Optional[HttpUrl] = None


# --- [2. Form 데이터를 읽어서 모델로 변환하는 의존성 함수들] ---

def signup_form_reader(
    email: Annotated[EmailStr, Form(...)],
    password: Annotated[str, Form(...)],
    password_confirm: Annotated[str, Form(...)],
    nickname: Annotated[Optional[str], Form(...)] = None,
    profile_image_url: Annotated[Optional[HttpUrl], Form(...)] = None
) -> UserSignUp:
    return UserSignUp(
        email=email,
        password=password,
        password_confirm=password_confirm,
        nickname=nickname,
        profile_image_url=profile_image_url
    )

def login_form_reader(
    email: Annotated[EmailStr, Form(..., alias="username")], # 폼에서 'email'로 받아도 username 필드에 매핑
    password: Annotated[str, Form(...)]
) -> UserLogin:
    return UserLogin(username=email, password=password)

def update_form_reader(
    email: Annotated[Optional[EmailStr], Form(...)] = None,
    password: Annotated[Optional[str], Form(...)] = None,
    nickname: Annotated[Optional[str], Form(...)] = None,
    profile_image_url: Annotated[Optional[HttpUrl], Form(...)] = None
) -> UserUpdate:
    return UserUpdate(
        email=email,
        password=password,
        nickname=nickname,
        profile_image_url=profile_image_url
    )

from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, Field, HttpUrl, model_validator
from fastapi import Form

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

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(...),
        password: str = Form(...),
        password_confirm: str = Form(...),
        nickname: Optional[str] = Form(None),
        profile_image_url: Optional[HttpUrl] = Form(None),
    ):
        return cls(**locals())

class UserLogin(BaseModel):
    username : EmailStr
    password: str

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(...),
        password: str = Form(...)
    ):
        return cls(username =email, password=password)

class UserUpdate(BaseModel):
    # 수정하고 싶은 필드만 선택적으로 받을 수 있게 Optional 처리
    email: Annotated[Optional[EmailStr], Field(description="사용자 이메일")] = None
    password: Annotated[Optional[str], Field(min_length=8, max_length=50)] = None
    nickname: Annotated[Optional[str], Field(min_length=2, max_length=20)] = None
    profile_image_url: Optional[HttpUrl] = None

    @classmethod
    def as_form(
        cls,
        email: Optional[EmailStr] = Form(None),
        nickname: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        profile_image_url: Optional[HttpUrl] = Form(None)
    ):
        return cls(**locals())
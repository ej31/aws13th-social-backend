from pydantic import BaseModel, field_validator, EmailStr
from fastapi import Form, File, UploadFile
import re

class SignupForm(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    profile_image: UploadFile | None

    #비밀번호 검증 해서 받기
    @field_validator('password')
    @classmethod
    def password_validator(cls, v: str):
            if len(v) < 8:
                raise ValueError("USERS_422_02: password must be longer than 8 characters")
            if len(v) > 20:
                raise ValueError("USERS_422_02: password cannot be longer than 20 characters")
            if not v.isascii():
                raise ValueError("USERS_422_02: password must contain at least one uppercase letter, one lowercase letter and one number")
            if " " in v:
                raise ValueError("USERS_422_02: password cannot contain spaces")
            if not re.search(r"[a-z]", v):
                raise ValueError("USERS_422_02: password must contain a lowercase letter")
            if not re.search(r"[0-9]", v):
                raise ValueError("USERS_422_02: password must contain a number")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
                raise ValueError("USERS_422_02: password must contain a special character")

            return v

    #닉네임 검증 해서 받기
    @field_validator('nickname')
    @classmethod
    def nickname_validator(cls, v: str):
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("USERS_422_03: nickname cannot contain special characters")
        if len(v) < 1:
            raise ValueError("USERS_422_03: nickname must be longer than 1 characters")
        if len(v) > 20:
            raise ValueError("USERS_422_03: nickname cannot be longer than 20 characters")
        return v
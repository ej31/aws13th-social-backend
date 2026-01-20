from pydantic import BaseModel, field_validator
from fastapi import UploadFile, File
import re

class SignupForm(BaseModel):
    email: str
    password: str
    nickname: str
    profile_image: UploadFile | None = File(None)

    #이메일 검증 로직
    @field_validator('email')
    @classmethod
    def email_validator(cls, v: str):
            v = v.strip()
            if not v:
                raise ValueError("email is empty")
            if not "@" in v:
                raise ValueError("email must have @")

            local, sep ,domain = v.partition("@")
            if not local or not domain:
                raise ValueError("email must have local and domain")
            if not "." in domain:
                raise ValueError("email must have domain with .")
            if ".." in v:
                raise ValueError("consecutive dots not allowed")
            if len(local) > 64:
                raise ValueError("local part of email cannot be longer than 64 characters")
            if len(domain) > 255:
                raise ValueError("domain part of email cannot be longer than 255 characters")

            return v

    #비밀번호 검증 로직
    @field_validator('password')
    @classmethod
    def password_validator(cls, v: str):
            if len(v) < 8:
                raise ValueError("password must be longer than 8 characters")
            if len(v) > 20:
                raise ValueError("password cannot be longer than 20 characters")
            if " " in v:
                raise ValueError("password cannot contain spaces")
            if not re.search(r"[a-z]", v):
                raise ValueError("password must contain a lowercase letter")
            if not re.search(r"[0-9]", v):
                raise ValueError("password must contain a number")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
                raise ValueError("password must contain a special character")

            return v

    #닉네임 검증 로직
    @field_validator('nickname')
    @classmethod
    def nickname_validator(cls, v: str):
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("nickname cannot only contain special characters")
        if len(v) < 1:
            raise ValueError("nickname must be longer than 1 characters")
        if len(v) > 20:
            raise ValueError("nickname cannot be longer than 20 characters")

    #프로필 이미지 검증 로직
    @field_validator('profile_image')
    @classmethod
    def profile_image_validator(cls, v: UploadFile | None):
        if v is None:
            return None

        limit_size = 10 * 1024 * 1024
        if v.size > limit_size:
            raise ValueError("profile image size must be less than 10MB")

        allowed_types = ["image/jpeg", "image/png", "image/jpg"]

        if v.content_type not in allowed_types:
            raise ValueError("profile image must be jpeg, png or jpg")

        return v

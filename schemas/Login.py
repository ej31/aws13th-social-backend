from pydantic import BaseModel, field_validator, EmailStr


class LoginForm(BaseModel):
    email: EmailStr
    password: str

    #비밀번호 검증 해서 받기
    @field_validator('password')
    @classmethod
    def validate_password_not_empty(cls, v: str):
        if not v or not v.strip():
            raise ValueError("비밀번호를 입력해주세요.")
        return v


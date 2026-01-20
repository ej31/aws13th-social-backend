from pydantic import BaseModel
import re

class Pagination(BaseModel):
    page: int
    limit: int
    total: int

def validate_password_logic(v: str) -> str:
    """
    공통 비밀번호 정책 로직 (예: 8자 이상, 특수문자 포함 등)
    """
    if len(v) < 8:
        raise ValueError("비밀번호는 최소 8자 이상이어야 합니다.")
    if not re.search(r'[A-Za-z]', v):
        raise ValueError('비밀번호에 영문자가 포함되어야 합니다')
    if not re.search(r'\d', v):
        raise ValueError('비밀번호에 숫자가 포함되어야 합니다')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>₩]', v):
        raise ValueError('비밀번호에 특수문자가 포함되어야 합니다')
    return v
    return v
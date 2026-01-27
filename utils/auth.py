import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    # bcrypt 입력 길이 문제 해결
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    로그인 시 입력 된 비밀번호와 저장된 해시를 비교함
    """

    return pwd_context.verify(plain_password, hashed_password)

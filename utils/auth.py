import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    # bcrypt 입력 길이 문제 해결
    password_bytes = password.encode("utf-8")
    sha256_hash = hashlib.sha256(password_bytes).hexdigest()

    #bcrypt 해싱
    return pwd_context.hash(sha256_hash)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")
    sha256_hash = hashlib.sha256(password_bytes).hexdigest()
    return pwd_context.verify(sha256_hash, hashed_password)

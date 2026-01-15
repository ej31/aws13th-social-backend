from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os
from datetime import datetime,timedelta
from jose import jwt
from dotenv import load_dotenv
# 해시 객체 생성
ph = PasswordHasher()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)

def get_password_hash(password: str) -> str:

    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:

    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

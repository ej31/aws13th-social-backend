from hashids import Hashids
from jose import jwt
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta, timezone

from common.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

hashids = Hashids(salt=settings.HASHIDS_SALT,min_length=8)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str,hashed_password: str ) -> bool:
    return pwd_context.verify(password, hashed_password)

def encode_id(id: int) -> str:
    return hashids.encode(id)

def decode_id(id: str) -> int:
    decoded = hashids.decode(id)
    return decoded[0] if decoded else None

def create_access_token(subject:str):
    minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode = {"exp": expire,
                 "sub":str(subject)}

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.algorithm
    )
    return encoded_jwt
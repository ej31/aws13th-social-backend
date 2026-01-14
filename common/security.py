from dotenv import load_dotenv
from hashids import Hashids
from jose import jwt
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

hashids = Hashids(salt="secret-key",min_length=8)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str,hashed_password: str ) -> bool:
    return pwd_context.verify(password, hashed_password)

def encode_id(id: int) -> str:
    return hashids.encode(id)

def decode_id(id: str) -> tuple:
    return hashids.decode(id)

def get_next_id_hash(db:list) -> str:
    if not db:
        return encode_id(1)

    id_numbers = []

    for user in db:
        decoded_id = decode_id(user["id"])
        if decoded_id:
            id_numbers.append(decoded_id[0])

    #DB에 데이터가 있는데 정상적인 숫자가 없으면 1번 시작
    if not id_numbers:
        return encode_id(1)

    next_number = max(id_numbers) + 1

    return encode_id(next_number)

def create_access_token(subject:str):
    minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    expire = datetime.utcnow() + timedelta(minutes=minutes)
    to_encode = {"exp": expire,
                 "sub":str(subject)}

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt
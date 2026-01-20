import bcrypt
import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

def create_access_token(data: dict):
    """사용자 정보(Payload)를 담은 JWT 토큰 생성"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    """토큰을 해석하여 사용자 정보를 반환"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except JWTError:
        return None

def hash_password(password: str) -> str:
    """비밀번호를 안전하게 해싱합니다 (bcrypt 직접 사용)."""
    # 1. 입력받은 문자열 비밀번호를 바이트(bytes) 형태로 변환
    pwd_bytes = password.encode('utf-8')
    # 2. 솔트(Salt) 생성
    salt = bcrypt.gensalt(rounds=12)
    # 3. 해싱 처리
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # 4. DB 저장을 위해 다시 문자열로 변환(decode)해서 반환
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문 비밀번호와 해싱된 비밀번호를 비교합니다."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

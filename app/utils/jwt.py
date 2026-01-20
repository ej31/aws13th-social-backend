from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET_KEY = "CHANGE_ME_TO_RANDOM_LONG_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    exp_dt = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": subject,
        "exp": int(exp_dt.timestamp()),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    sub = payload["sub"]

    if not sub:
        raise JWTError("Invalid token")

    return sub
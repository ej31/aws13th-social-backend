from datetime import datetime, timedelta, timezone
from jose import jwt
import uuid
from core.config import jwt_settings


def create_access_token(user_id: str):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = jwt.encode(payload, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
    return token, jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
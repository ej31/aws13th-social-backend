from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

router = APIRouter(prefix="/auth",tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto") #bcypt는 72바이트밖에 지원을 안해서 bcrypt_sha256로 변경

@router.post("/token", summary= "로그인", description="사용자 인증 후 액세스 토큰을 발급함. 로그인은 토큰 리소스 생성으로 모델링",tags=["auth"])
async def login_for_access_token():
    return

# 비밀번호 해싱
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
# 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from app.schemas.users import UserLoginRequest
from app.utils.jwt import create_access_token
from app.schemas.common import TokenResponse
from app.utils.data import find_user_by_email

router = APIRouter(prefix="/auth",tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto") #bcypt는 72바이트밖에 지원을 안해서 bcrypt_sha256로 변경

@router.post("/token", response_model = TokenResponse , summary= "로그인", description="사용자 인증 후 액세스 토큰을 발급함. 로그인은 토큰 리소스 생성으로 모델링",tags=["auth"])
async def login_for_access_token(body: UserLoginRequest):
    user = find_user_by_email(body.email)

    if user.get("is_deleted"):
        raise HTTPException(401, "탈퇴한 계정입니다.")

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "유저 정보를 찾을 수 없습니다."
        )

    hashed_pw = user.get("hash_password")
    if not hashed_pw:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "서버에 저장된 비밀번호 정보가 올바르지 않습니다."
        )

    if not verify_password(body.password, user["hash_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "비밀번호가 올바르지 않습니다."
        )

    token = create_access_token(subject=user["email"])
    return TokenResponse(access_token=token, token_type="bearer")

# 비밀번호 해싱
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
# 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


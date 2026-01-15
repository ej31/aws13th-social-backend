from typing import Annotated

from fastapi import Depends, HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer


from common.security import decode_access_token
from repositories.user_repository import UserRepository
from services.user_service import UserService

security = HTTPBearer()

def get_user_repo() -> UserRepository:
    return UserRepository()

def get_auth_service(
        repo: Annotated[UserRepository, Depends(get_user_repo)]
) -> UserService:
    return UserService(user_repo = repo)

#jwt 인증된 사용자인지 확인
async def get_current_user(
        auth: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        user_repo : Annotated[UserRepository, Depends(get_user_repo)]
) -> dict:
    token = auth.credentials
    email = decode_access_token(token)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 토큰을 찾을 수 없습니다.",
        )
    user = user_repo.find_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다."
        )

    return user
from typing import Annotated, Optional

from fastapi import Depends, HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import get_db
from common.jwt import decode_access_token
from models.base import User
from repositories.comment_repository import CommentRepository
from repositories.like_repository import LikeRepository
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from services.comment_service import CommentService
from services.like_service import LikeService
from services.post_service import PostService
from services.user_service import UserService

#HTTP 헤더에서 Beare Token이 있는지 검사한다.
#Sweager UI에 오른쪽에 Authorize 버튼이 생긴다.
security = HTTPBearer()

#비인증 사용자도 게시글이나 댓글을 조회할 수 있게 한다.
optional_security = HTTPBearer(auto_error=False)

def get_user_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return UserRepository(db)

def get_post_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> PostRepository:
    return PostRepository(db)

def get_like_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> LikeRepository:
    return LikeRepository(db)

def get_comment_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> CommentRepository:
    return CommentRepository(db)

def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repo)]
) -> UserService:
    return UserService(user_repo=user_repo)

def get_post_service(
    post_repo: Annotated[PostRepository, Depends(get_post_repo)],
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
    like_repo: Annotated[LikeRepository, Depends(get_like_repo)]
) -> PostService:
    return PostService(post_repo=post_repo, user_repo=user_repo, like_repo=like_repo)

def get_like_service(
    like_repo: Annotated[LikeRepository, Depends(get_like_repo)],
    post_repo: Annotated[PostRepository, Depends(get_post_repo)]
) -> LikeService:
    return LikeService(like_repo=like_repo, post_repo=post_repo)

def get_comment_service(
    comment_repo: Annotated[CommentRepository, Depends(get_comment_repo)],
    post_repo: Annotated[PostRepository, Depends(get_post_repo)],
    user_repo: Annotated[UserRepository, Depends(get_user_repo)]
) -> CommentService:
    return CommentService(
        comment_repository=comment_repo,
        post_repository=post_repo,
        user_repository=user_repo
    )

async def get_current_optional_user(
        auth: Annotated[HTTPAuthorizationCredentials | None, Depends(optional_security)],
        user_repo : Annotated[UserRepository, Depends(get_user_repo)]
) -> Optional[User] | None:

    #토큰 자체가 없는 경우 (비 인증 사용자)
    if not auth:
        return None

    email = decode_access_token(auth.credentials)

    user = await user_repo.find_by_email(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유저를 찾을 수 없습니다."
        )
    return user

#jwt 인증된 사용자인지 확인
async def get_current_user(
        user: Annotated[Optional[User], Depends(get_current_optional_user)],
) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요한 서비스입니다."
        )
    return user
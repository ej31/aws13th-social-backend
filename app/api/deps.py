"""
API 공통 의존성
- Repository 주입
- 인증 사용자 조회
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import get_settings
from app.core.security import decode_access_token
from app.repositories.user import UserRepository
from app.repositories.post import PostRepository
from app.repositories.comment import CommentRepository
from app.repositories.like import LikeRepository

settings = get_settings()

# HTTP Bearer 토큰 스키마
security = HTTPBearer()


# Repository 의존성
# 각 리포지토리(User, Post, Comment, Like)를 생성하여 반환
# DB 연결은 각 Repository 내부에서 get_database()로 자동 처리

def get_user_repository() -> UserRepository:
    """UserRepository 의존성 주입"""
    return UserRepository()


def get_post_repository() -> PostRepository:
    """PostRepository 의존성 주입"""
    return PostRepository()


def get_comment_repository() -> CommentRepository:
    """CommentRepository 의존성 주입"""
    return CommentRepository()


def get_like_repository() -> LikeRepository:
    """LikeRepository 의존성 주입"""
    return LikeRepository()


# 인증 의존성
# 요청이 올 때마다 JWT 토큰을 검사하여 현재 사용자가 누구인지 식별

# 1. 토큰 추출: HTTPBearer를 통해 HTTP Header의 Authorization: Bearer <token>에서 토큰을 가져옴
# 2. 디코딩: decode_access_token으로 토큰의 유효성 검사
# 3. DB 조회: 토큰 속 user_id로 실제 사용자가 DB에 존재하는지 확인
# 4. 예외 처리: 토큰이 없거나, 유효하지 않거나, 사용자가 없으면 즉시 401 Unauthorized 에러를 던져 API 실행을 중단

def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> dict:
    """
    현재 로그인한 사용자 정보 조회
    """
    # JWT 토큰 디코딩
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 사용자 조회
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰에 사용자 정보가 없습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_repo.find_by_user_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

# 선택적 인증
# 비로그인 사용자도 접근할 수 있는 페이지

def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        HTTPBearer(auto_error=False)
    ),
    user_repo: UserRepository = Depends(get_user_repository)
) -> dict | None:
    """
    현재 로그인한 사용자 정보 조회 (선택적)
    - 인증이 필수가 아닌 경우 사용
    - 토큰이 없거나 유효하지 않으면 None 반환
    """
    if credentials is None:
        return None
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        return None
    
    user_id = payload.get("user_id")
    if user_id is None:
        return None
    
    return user_repo.find_by_user_id(user_id)


# 타입 별칭
CurrentUser = Annotated[dict, Depends(get_current_user)]
CurrentUserOptional = Annotated[dict | None, Depends(get_current_user_optional)]
UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
PostRepo = Annotated[PostRepository, Depends(get_post_repository)]
CommentRepo = Annotated[CommentRepository, Depends(get_comment_repository)]
LikeRepo = Annotated[LikeRepository, Depends(get_like_repository)]
"""
API v1 라우터
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .posts import router as posts_router
from .comments import router as comments_router
from .likes import router as likes_router

# v1 통합 라우터
api_router = APIRouter()

# 각 라우터 등록
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(posts_router, prefix="/posts", tags=["posts"])
api_router.include_router(comments_router, tags=["comments"])
api_router.include_router(likes_router, tags=["likes"])
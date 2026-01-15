"""
Pydantic 스키마 모듈
"""
from .common import APIResponse, PaginationResponse, PaginationParams
from .user import (
    UserSignupRequest,
    UserUpdateRequest,
    UserProfileResponse,
    UserPublicResponse,
    UserAuthorInfo
)
from .auth import (
    LoginRequest,
    LoginResponse,
    LoginUserInfo
)
from .post import (
    PostCreateRequest,
    PostUpdateRequest,
    PostResponse,
    PostListResponse,
    PostAuthorInfo
)
from .comment import (
    CommentCreateRequest,
    CommentUpdateRequest,
    CommentResponse,
    CommentListResponse,
    MyCommentResponse,
    MyCommentListResponse
)
from .like import (
    LikeResponse,
    LikeStatusResponse,
    LikedPostResponse,
    LikedPostListResponse
)

__all__ = [
    # Common
    "APIResponse",
    "PaginationResponse",
    "PaginationParams",

    # User
    "UserSignupRequest",
    "UserUpdateRequest",
    "UserProfileResponse",
    "UserPublicResponse",
    "UserAuthorInfo",

    # Auth
    "LoginRequest",
    "LoginResponse",
    "LoginUserInfo",

    # Post
    "PostCreateRequest",
    "PostUpdateRequest",
    "PostResponse",
    "PostListResponse",
    "PostAuthorInfo",

    # Comment
    "CommentCreateRequest",
    "CommentUpdateRequest",
    "CommentResponse",
    "CommentListResponse",
    "MyCommentResponse",
    "MyCommentListResponse",

    # Like
    "LikeResponse",
    "LikeStatusResponse",
    "LikedPostResponse",
    "LikedPostListResponse"
]
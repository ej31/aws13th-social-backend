"""
좋아요 관련 스키마
"""
from datetime import datetime
from pydantic import BaseModel, Field
from .user import UserAuthorInfo
from .common import PaginationResponse

class LikeResponse(BaseModel):
    """
    좋아요 등록 응답

    Attributes:
        post_id: 게시글 ID
        user_id: 사용자 ID
        created_at: 생성일시
    """
    post_id: int = Field(description="게시글 ID")
    user_id: int = Field(description="사용자 ID")
    created_at: datetime = Field(description="생성일시")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "post_id": 123,
                    "user_id": 124,
                    "created_at": "2026-01-06T11:00:00Z"
                }
            ]
        }
    }

class LikeStatusResponse(BaseModel):
    """
    좋아요 상태 응답

    Attributes:
        post_id: 게시글 ID
        total_likes: 총 좋아요 수
        is_liked: 현재 사용자의 좋아요 여부
    """
    post_id: int = Field(description="게시글 ID")
    total_likes: int = Field(ge=0, description="총 좋아요 수")
    is_liked: bool = Field(description="현재 사용자의 좋아요 여부")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "post_id": 123,
                    "total_likes": 42,
                    "is_liked": True
                }
            ]
        }
    }

class LikedPostResponse(BaseModel):
    """
    내가 좋아요한 게시글 응답

    Attributes:
        post_id: 게시글 ID
        title: 게시글 제목
        content: 게시글 내용
        author: 작성자 정보
        views: 조회수
        likes: 좋아요 수
        comments_count: 댓글 수
        liked_at: 좋아요 누른 시간
        created_at: 게시글 생성일시
    """
    post_id: int = Field(description="게시글 ID")
    title: str = Field(description="게시글 제목")
    content: str = Field(description="게시글 내용")
    author: UserAuthorInfo = Field(description="작성자 정보")
    views: int = Field(ge=0, description="조회수")
    likes: int = Field(ge=0, description="좋아요 수")
    comments_count: int = Field(ge=0, description="댓글 수")
    liked_at: datetime = Field(description="좋아요 누른 시간")
    created_at: datetime = Field(description="게시글 생성일시")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "post_id": 123,
                    "title": "클라우드 커뮤니티에 오신 것을 환영합니다",
                    "content": "게시글 내용입니다...",
                    "author": {
                        "user_id": 123,
                        "nickname": "클라우드유저",
                        "profile_image": "https://example.com/profile.jpg"
                    },
                    "views": 42,
                    "likes": 5,
                    "comments_count": 3,
                    "liked_at": "2026-01-06T11:00:00Z",
                    "created_at": "2026-01-06T10:00:00Z"
                }
            ]
        }
    }

class LikedPostListResponse(BaseModel):
    """
    내가 좋아요한 게시글 목록 응답

    Attributes:
        data: 내가 좋아요한 게시글 목록
        pagination: 페이지네이션 정보
    """
    data: list[LikedPostResponse] = Field(description="내가 좋아요한 게시글 목록")
    pagination: PaginationResponse = Field(description="페이지네이션 정보")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": [
                        {
                            "post_id": 123,
                            "title": "클라우드 커뮤니티에 오신 것을 환영합니다",
                            "content": "게시글 내용입니다...",
                            "author": {
                                "user_id": 123,
                                "nickname": "클라우드유저",
                                "profile_image": "https://example.com/profile.jpg"
                            },
                            "views": 42,
                            "likes": 5,
                            "comments_count": 3,
                            "liked_at": "2026-01-06T11:00:00Z",
                            "created_at": "2026-01-06T10:00:00Z"
                        }
                    ],
                    "pagination": {
                        "page": 1,
                        "limit": 20,
                        "total": 15,
                        "total_pages": 1
                    }
                }
            ]
        }
    }
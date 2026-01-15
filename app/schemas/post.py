"""
게시글 관련 스키마
"""
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from ..utils.validators import validate_post_title, validate_post_content
from .user import UserAuthorInfo
from .common import PaginationResponse

class PostCreateRequest(BaseModel):
    """
    게시글 작성 요청

    Attributes:
        title: 게시글 제목 (1~200자)
        content: 게시글 내용 (1~10000자)
    """
    title: str = Field(min_length=1, max_length=200, description="게시글 제목")
    content: str = Field(min_length=1, max_length=10000, description="게시글 내용")

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        return validate_post_title(v)

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        return validate_post_content(v)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "클라우드 커뮤니티에 오신 것을 환영합니다",
                    "content": "게시글 내용입니다. 여기에는 게시글의 전체 내용이 포함됩니다..."
                }
            ]
        }
    }

class PostUpdateRequest(BaseModel):
    """
    게시글 수정 요청

    Attributes:
        title: 변경할 게시글 제목 (선택, 1~200자)
        content: 변경할 게시글 내용 (선택, 1~10000자)
    """
    title: str | None = Field(default=None, min_length=1, max_length=200, description="게시글 제목")
    content: str | None = Field(default=None, min_length=1, max_length=10000, description="게시글 내용")

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str | None) -> str | None:
        if v is not None:
            return validate_post_title(v)
        return v

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str | None) -> str | None:
        if v is not None:
            return validate_post_content(v)
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "수정된 제목",
                    "content": "수정된 내용입니다..."
                }
            ]
        }
    }

class PostAuthorInfo(UserAuthorInfo):
    """
    게시글 작성자 정보 (UserAuthorInfo 상속)
    """
    pass

class PostResponse(BaseModel):
    """
    게시글 응답

    Attributes:
        post_id: 게시글 ID
        title: 게시글 제목
        content: 게시글 내용
        author: 작성자 정보
        views: 조회수
        likes: 좋아요 수
        comments_count: 댓글 수
        created_at: 생성일시
        updated_at: 수정일시
    """
    post_id: int = Field(description="게시글 ID")
    title: str = Field(description="게시글 제목")
    content: str = Field(description="게시글 내용")
    author: PostAuthorInfo = Field(description="작성자 정보")
    views: int = Field(ge=0, description="조회수")
    likes: int = Field(ge=0, description="좋아요 수")
    comments_count: int = Field(ge=0, description="댓글 수")
    created_at: datetime = Field(description="생성일시")
    updated_at: datetime = Field(description="수정일시")

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
                    "created_at": "2026-01-06T10:00:00Z",
                    "updated_at": "2026-01-06T10:00:00Z"
                }
            ]
        }
    }

class PostListResponse(BaseModel):
    """
    게시글 목록 응답

    Attributes:
        data: 게시글 목록
        pagination: 페이지네이션 정보
    """
    data: list[PostResponse] = Field(description="게시글 목록")
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
                            "created_at": "2026-01-06T10:00:00Z",
                            "updated_at": "2026-01-06T10:00:00Z"
                        }
                    ],
                    "pagination": {
                        "page": 1,
                        "limit": 20,
                        "total": 150,
                        "total_pages": 8
                    }
                }
            ]
        }
    }
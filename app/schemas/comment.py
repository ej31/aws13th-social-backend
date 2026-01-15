"""
댓글 관련 스키마
"""
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from ..utils.validators import validate_comment_content
from .user import UserAuthorInfo
from .common import PaginationResponse

class CommentCreateRequest(BaseModel):
    """
    댓글 작성 요청

    Attributes:
        content: 댓글 내용 (1~500자)
    """
    content: str = Field(min_length=1, max_length=500, description="댓글 내용")

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        return validate_comment_content(v)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "content": "좋은 글 감사합니다!"
                }
            ]
        }
    }

class CommentUpdateRequest(BaseModel):
    """
    댓글 수정 요청

    Attributes:
        content: 변경할 댓글 내용 (1~500자)
    """
    content: str = Field(min_length=1, max_length=500, description="댓글 내용")

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        return validate_comment_content(v)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "content": "수정된 댓글 내용입니다."
                }
            ]
        }
    }

class CommentResponse(BaseModel):
    """
    댓글 응답

    Attributes:
        comment_id: 댓글 ID
        post_id: 게시글 ID
        content: 댓글 내용
        author: 작성자 정보
        created_at: 생성일시
        updated_at: 수정일시
    """
    comment_id: int = Field(description="댓글 ID")
    post_id: int = Field(description="게시글 ID")
    content: str = Field(description="댓글 내용")
    author: UserAuthorInfo = Field(description="작성자 정보")
    created_at: datetime = Field(description="생성일시")
    updated_at: datetime = Field(description="수정일시")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "comment_id": 123,
                    "post_id": 123,
                    "content": "좋은 글 감사합니다!",
                    "author": {
                        "user_id": 124,
                        "nickname": "개발자",
                        "profile_image": "https://example.com/dev.jpg"
                    },
                    "created_at": "2026-01-06T11:00:00Z",
                    "updated_at": "2026-01-06T11:00:00Z"
                }
            ]
        }
    }

class CommentListResponse(BaseModel):
    """
    댓글 목록 응답

    Attributes:
        data: 댓글 목록
        pagination: 페이지네이션 정보
    """
    data: list[CommentResponse] = Field(description="댓글 목록")
    pagination: PaginationResponse = Field(description="페이지네이션 정보")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": [
                        {
                            "comment_id": 123,
                            "post_id": 123,
                            "content": "좋은 글 감사합니다!",
                            "author": {
                                "user_id": 124,
                                "nickname": "개발자",
                                "profile_image": "https://example.com/dev.jpg"
                            },
                            "created_at": "2026-01-06T11:00:00Z",
                            "updated_at": "2026-01-06T11:00:00Z"
                        }
                    ],
                    "pagination": {
                        "page": 1,
                        "limit": 20,
                        "total": 50,
                        "total_pages": 3
                    }
                }
            ]
        }
    }

class MyCommentResponse(BaseModel):
    """
    내가 쓴 댓글 응답 (추가 정보 포함)

    Attributes:
        comment_id: 댓글 ID
        post_id: 게시글 ID
        post_title: 게시글 제목 (어떤 게시글에 단 댓글인지 확인용)
        content: 댓글 내용
        created_at: 생성일시
        updated_at: 수정일시
    """
    comment_id: int = Field(description="댓글 ID")
    post_id: int = Field(description="게시글 ID")
    post_title: str = Field(description="게시글 제목")
    content: str = Field(description="댓글 내용")
    created_at: datetime = Field(description="생성일시")
    updated_at: datetime = Field(description="수정일시")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "comment_id": 123,
                    "post_id": 123,
                    "post_title": "클라우드 커뮤니티에 오신 것을 환영합니다",
                    "content": "좋은 글 감사합니다!",
                    "created_at": "2026-01-06T11:00:00Z",
                    "updated_at": "2026-01-06T11:00:00Z"
                }
            ]
        }
    }

class MyCommentListResponse(BaseModel):
    """
    내가 쓴 댓글 목록 응답

    Attributes:
        data: 내가 쓴 댓글 목록
        pagination: 페이지네이션 정보
    """
    data: list[MyCommentResponse] = Field(description="내가 쓴 댓글 목록")
    pagination: PaginationResponse = Field(description="페이지네이션 정보")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": [
                        {
                            "comment_id": 123,
                            "post_id": 123,
                            "post_title": "클라우드 커뮤니티에 오신 것을 환영합니다",
                            "content": "좋은 글 감사합니다!",
                            "created_at": "2026-01-06T11:00:00Z",
                            "updated_at": "2026-01-06T11:00:00Z"
                        }
                    ],
                    "pagination": {
                        "page": 1,
                        "limit": 20,
                        "total": 30,
                        "total_pages": 2
                    }
                }
            ]
        }
    }
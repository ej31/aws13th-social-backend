from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from common.security import encode_id

class PostsBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, description="게시물의 제목")
    content: str = Field(..., min_length=1, description="게시물의 내용")

class PostsAuthorResponse(BaseModel):
    id: str
    nickname: str

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("id")
    def serialize_id(self, v: int) -> str:
        return encode_id(v)

class PostsResponse(PostsBase):
    id: str = Field(..., description="게시물의 고유 ID")
    author: PostsAuthorResponse
    is_liked: bool = Field(False, description="현재 사용자의 좋아요 여부")
    like_count: int = Field(0, description="좋아요 총 개수")
    views: int = Field(0, description="조회수")
    created_at: datetime
    # updated_at은 DB 모델에 존재한다면 추가

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("id")
    def serialize_id(self, v: int) -> str:
        return encode_id(v)

class PostsResponseDetail(PostsResponse):
    # comments: List[CommentResponse] = [] # 댓글 기능 활성화 시 추가
    pass

class PostsCreateRequest(PostsBase):
    pass

class PostsUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1)
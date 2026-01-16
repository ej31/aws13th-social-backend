# schemas/posts.py
from pydantic import BaseModel
from datetime import datetime
from app.schemas.common import Pagination


class Author(BaseModel):
    id: int
    nickname: str


# ===== Requests =====
class PostCreateRequest(BaseModel):
    title: str
    content: str


class PostUpdateRequest(BaseModel):
    title: str | None = None
    content: str | None = None


# ===== Responses =====
class PostSummary(BaseModel):
    id: int
    title: str
    created_at: datetime


class PostSearchItem(BaseModel):
    id: int
    title: str
    content: str


class PostListItem(BaseModel):
    id: int
    title: str
    author: Author
    created_at: datetime


class PostDetail(BaseModel):
    id: int
    title: str
    content: str
    author: Author
    created_at: datetime


class PostCreateData(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime


class PostUpdateData(BaseModel):
    id: int
    title: str
    content: str
    updated_at: datetime


class PostListData(BaseModel):
    list: list[PostListItem]
    pagination: Pagination


class PostListResponse(BaseModel):
    status: str
    data: PostListData


class PostSearchData(BaseModel):
    list: list[PostSearchItem]
    pagination: Pagination


class PostSearchResponse(BaseModel):
    status: str
    data: PostSearchData


class PostDetailResponse(BaseModel):
    status: str
    data: PostDetail


class PostCreateResponse(BaseModel):
    status: str
    data: PostCreateData


class PostUpdateResponse(BaseModel):
    status: str
    data: PostUpdateData


class MyPostListData(BaseModel):
    list: list[PostSummary]
    pagination: Pagination


class MyPostListResponse(BaseModel):
    status: str
    data: MyPostListData

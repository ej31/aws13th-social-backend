# schemas/comments.py
from pydantic import BaseModel
from datetime import datetime


class MyCommentItem(BaseModel):
    id: int
    comment: str
    created_at: datetime


class PostCommentItem(BaseModel):
    # 특정 게시글 댓글 목록 조회는 id 없이 내려옴 :contentReference[oaicite:5]{index=5}
    nickname: str
    comment: str
    created_at: datetime


# ===== Requests =====
class CommentCreateRequest(BaseModel):
    comment: str


class CommentUpdateRequest(BaseModel):
    comment: str


# ===== Responses =====
class MyCommentListData(BaseModel):
    list: list[MyCommentItem]


class MyCommentListResponse(BaseModel):
    status: str
    data: MyCommentListData


class PostCommentListData(BaseModel):
    list: list[PostCommentItem]


class PostCommentListResponse(BaseModel):
    status: str
    data: PostCommentListData


class CommentCreateData(BaseModel):
    id: int
    comment: str
    created_at: datetime


class CommentCreateResponse(BaseModel):
    status: str
    data: CommentCreateData


class CommentUpdateData(BaseModel):
    id: int
    comment: str
    updated_at: datetime


class CommentUpdateResponse(BaseModel):
    status: str
    data: CommentUpdateData

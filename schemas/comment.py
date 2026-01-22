from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# POST /posts/{post_id}/comments
class CommentCreate(BaseModel):
    comment: str = Field(..., min_length=1, description="작성할 댓글 내용")

# PATCH /comments/{comment_id}
class CommentUpdate(BaseModel):
    comment: str = Field(..., min_length=1, description="수정할 댓글 내용")

# GET /users/me/comments (내 댓글 목록)
# GET /posts/{post_id}/comments (게시글 댓글 목록)
class CommentListResponse(BaseModel):
    id: int
    nickname: str
    created_at: datetime

# POST /posts/{post_id}/comments (작성 직후 응답)
# PATCH /comments/{comment_id} (수정 직후 응답)
class CommentDetailResponse(BaseModel):
    id: int
    comment: str
    created_at: datetime
    # 수정 시
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
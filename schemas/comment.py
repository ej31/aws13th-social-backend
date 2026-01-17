from datetime import datetime

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    content: str = Field(...,min_length=1,max_length=255,description="댓글 내용")

class CommentCreateRequest(CommentBase):
    pass

class CommentUpdateRequest(CommentBase):
    pass

class AuthorResponse(BaseModel):
    id: str
    nickname: str

class CommentResponse(CommentBase):
    comment_id: int = Field(...,description="댓글의 ID")
    post_id: int = Field(...,description="게시물의 ID")
    author: AuthorResponse = Field(...,description="댓글 작성자의 내용")
    created_at: datetime = Field(...,description="생성 시간")
    updated_at: datetime | None = Field(None,description="수정 시간 (최초 생성시에는 null)")


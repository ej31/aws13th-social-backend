from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from common.security import encode_id

# 1. 공통 필드
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=255, description="댓글 내용")

# 2. 작성자 정보 (유저 객체에서 필요한 것만)
class AuthorResponse(BaseModel):
    id: int # 내부적으로 int, 나갈 때 str
    nickname: str

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("id")
    def serialize_id(self, v: int) -> str:
        return encode_id(v)

# 3. 댓글 응답
class CommentResponse(CommentBase):
    id: int = Field(..., description="댓글의 고유 ID")
    post_id: int = Field(..., description="게시물의 고유 ID")
    author: AuthorResponse = Field(..., description="댓글 작성자 정보")
    created_at: datetime
    updated_at: Optional[datetime] = None

    # SQLAlchemy 객체 호환 설정
    model_config = ConfigDict(from_attributes=True)

    # 댓글 ID와 게시물 ID 모두 클라이언트에게는 인코딩해서 보냅니다.
    @field_serializer("id", "post_id")
    def serialize_ids(self, v: int) -> str:
        return encode_id(v)

# 4. 생성 및 수정 요청
class CommentCreateRequest(CommentBase):
    pass

class CommentUpdateRequest(CommentBase):
    pass
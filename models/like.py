from pydantic import BaseModel,Field
from enum import Enum

class LikeTargetType(str, Enum):
    PostLike = "PostLike"
    CommentLike = "CommentLike"

class LikeCreate(BaseModel):
    target_type: LikeTargetType = Field(...,description="LikeTargetType")
    target_id: str

class LikeResponse(BaseModel):
    target_type: LikeTargetType
    target_id: str
    like_id: str
    user_id: str
    is_liked: bool  # True면 좋아요 추가, False면 좋아요 취소 (Toggle 방식일 때)
    total_likes: int
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
    is_liked: bool
    total_likes: int
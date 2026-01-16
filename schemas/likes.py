from pydantic import BaseModel
from datetime import datetime

class LikeCreate(BaseModel):
    postId: int

class LikeResponse(BaseModel):
    likeId: int
    postId: int
    userId: int
    createdAt: datetime

class LikeListItem(BaseModel):
    likeId: int
    postId: int
    title: str
    nickname: str
    createdAt: datetime

class LikeStatus(BaseModel):
    postId: int
    totalLikes: int
    isLiked: bool

from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostListItem(BaseModel):
    postId: int
    title: str
    content: str
    nickname: str
    viewCount: int
    likeCount: int
    createdAt: datetime

class PostDetail(BaseModel):
    postId: int
    title: str
    content: str
    nickname: str
    profileImage: str | None = None
    viewCount: int
    likeCount: int
    isLiked: bool
    createdAt: datetime
    updatedAt: datetime

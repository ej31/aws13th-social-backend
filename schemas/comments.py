from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    postId: int
    content: str

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    commentId: int
    postId: int
    content: str
    userId: int
    nickname: str
    createdAt: datetime

class MyCommentResponse(BaseModel):
    commentId: int
    postId: int
    postTitle: str
    content: str
    createdAt: datetime
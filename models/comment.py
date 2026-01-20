from datetime import datetime
from typing import Annotated, List

from pydantic import BaseModel, Field


class Comment(BaseModel):
    content: Annotated[str, Field(min_length=1,max_length=100)]

class CommentInternal(BaseModel):
    comment_id: str
    content: Annotated[str, Field(min_length=1,max_length=100)]

class CommentResponse(BaseModel):
    content: str
    comment_id: str
    post_id: str
    user_id: str
    created_at: datetime

class AllComments(BaseModel):
    total: int
    comments: List[CommentResponse]
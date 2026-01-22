from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# (POST /posts)
class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

# (PATCH /posts/{post_id})
class PostUpdate(BaseModel):

    content: Optional[str] = Field(None, min_length=1)

# (GET /posts?page=2&limit=10)
class PostListResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

# (GET /posts/{post_id})
class PostDetailResponse(BaseModel):
    id: int
    title: str
    content: str
    view_count: int
    created_at: datetime

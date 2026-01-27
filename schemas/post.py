
from pydantic import BaseModel

class PostCreate(BaseModel):
     title: str
     content: str

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author_id: int

class PostLikedOut(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: str | None = None
    like_count: int

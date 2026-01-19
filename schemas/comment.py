
from pydantic import BaseModel

class CommentCreate(BaseModel):
    post_id: int
    content: str

class CommentOut(BaseModel):
    id: int
    post_id: int
    content: str
    author_id: int
    created_at: str | None = None


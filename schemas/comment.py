
from pydantic import BaseModel

class CommentCreate(BaseModel):
    comment: str

class CommentOut(BaseModel):
    id: int
    post_id: int
    comment: str
    author_id: int
    created_at: str | None = None


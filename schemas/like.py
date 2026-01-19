
from pydantic import BaseModel

class LikeCreate(BaseModel):
    post_id: int

class LikeOut(BaseModel):
    id: int
    post_id: int
    user_id: int
    has_like: bool
    total_like_count: int
    post_count: int
from pydantic import BaseModel

from schemas.commons import Pagination, Count
from schemas.post import PostListItem


class LikeStatusResponse(BaseModel):
    liked: bool
    like_count: Count


class LikedPostsResponse(BaseModel):
    data: list[PostListItem]
    pagination: Pagination

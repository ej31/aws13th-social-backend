from datetime import datetime

# - [ ]  **내가 좋아요한 게시글 목록**: 로그인한 사용자가 좋아요 누른 게시글들 조회
from pydantic import BaseModel

from schemas.commons import PostId, UserId, Pagination
from schemas.post import Count, Title


class LikedListItem(BaseModel):
    post_id: PostId
    author: UserId
    title: Title
    view_count: Count
    like_cound: Count
    created_at: datetime


class ListPostILiked(BaseModel):
    data: list[LikedListItem]
    pagination: Pagination


class LikeStatusResponse(BaseModel):
    liked: bool
    like_count: Count

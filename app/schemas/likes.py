# schemas/likes.py
from pydantic import BaseModel
from datetime import datetime


class LikedPostItem(BaseModel):
    id: int
    title: str
    created_at: datetime


class LikeState(BaseModel):
    liked: bool
    like_count: int


class LikedPostListData(BaseModel):
    list: list[LikedPostItem]


class LikedPostListResponse(BaseModel):
    status: str
    data: LikedPostListData


# 좋아요 상태 확인 / 등록 / 취소는 status wrapper 없이 liked, like_count만 내려오는 형태 :contentReference[oaicite:6]{index=6}
class LikeStateResponse(BaseModel):
    liked: bool
    like_count: int

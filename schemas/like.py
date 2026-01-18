from pydantic import BaseModel, Field


class LikeStatusResponse(BaseModel):
    like_id: str = Field(...,description="좋아요 고유 식별자")
    post_id: str = Field(...,description="게시물 ID")
    is_liked: bool = Field(...,description="현재 사용자의 좋아요 여부")
    like_count: int = Field(...,description="해당 게시물의 좋아요 개수",ge=0)


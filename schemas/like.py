from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from common.security import encode_id

class LikeStatusResponse(BaseModel):
    # 좋아요를 누르지 않았을 때는 ID가 없을 수 있으므로 Optional 처리
    like_id: Optional[int] = Field(None, description="좋아요 고유 식별자 (HashID로 변환됨)")
    post_id: int = Field(..., description="게시물 ID (HashID로 변환됨)")
    is_liked: bool = Field(..., description="현재 사용자의 좋아요 여부")
    like_count: int = Field(..., description="해당 게시물의 총 좋아요 수", ge=0)

    # 1. SQLAlchemy 객체 대응 설정
    model_config = ConfigDict(from_attributes=True)

    # 2. 필드 시리얼라이저: ID들을 나갈 때 자동으로 인코딩함
    @field_serializer("like_id", "post_id")
    def serialize_ids(self, v: Optional[int]) -> Optional[str]:
        if v is None:
            return None
        return encode_id(v)

# LikeCreateInternal은 더 이상 사용하지 않으므로 삭제해도 무방합니다.
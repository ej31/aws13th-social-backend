from typing import TypeVar, Generic

from pydantic import BaseModel, Field

T = TypeVar("T")

#ge grater than or equal
class PaginationMeta(BaseModel):
    page: int = Field(...,ge=1,description="현재 페이지 번호")
    limit: int = Field(...,ge=1,description="페이지당 아이템 개수")
    total_items: int = Field(...,ge=0,description="전체 아이템 개수")
    total_pages: int = Field(...,ge=0,description="전체 페이지 수")

class PaginatedResponse(Generic[T], BaseModel):
    content: list[T] = Field(...,description="데이터 리스트")
    pagination: PaginationMeta
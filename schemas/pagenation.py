from typing import TypeVar, Generic, List

from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationMeta(BaseModel):
    page: int = Field(...,description="현재 페이지 번호")
    limit: int = Field(...,description="페이지당 아이템 개수")
    total_items: int = Field(...,description="전체 아이템 개수")
    total_pages: int = Field(...,description="전체 페이지 수")

class PaginatedResponse(Generic[T], BaseModel):
    content: List[T] = Field(...,description="데이터 리스트")
    pagination: PaginationMeta
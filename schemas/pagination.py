from typing import TypeVar, Generic

from pydantic import BaseModel, Field, computed_field

T = TypeVar("T")

#ge grater than or equal
class PaginationMeta(BaseModel):
    page: int = Field(...,ge=1,description="현재 페이지 번호")
    limit: int = Field(...,ge=1,description="페이지당 아이템 개수")
    total_items: int = Field(...,ge=0,description="전체 아이템 개수")

    #computed_filed의 경우 property로 만든 가짜 변수를 실제 데이터 필드인 것 처럼 취급한다.
    #API 응답에도 사용한다.
    #property의 경우 메서드를 변수(속성)처럼 다룰 수 있게 해준다.
    @computed_field
    @property
    def total_pages(self) -> int:
        if self.limit <= 0:
            return 0
        """
            나누기 전에 미리 가짜 데이터를 채워 넣는다.
            total_items + limit - 1) // limit
            total_items의 게시글이 11개 있다고 가정해보자
            왜 limit이 아니라 limit -1을 하는 이유는 
            만약 (10+5)//5 = 3이 되게 되었을 경우에 아무 내용도 없는 빈페이지 3이 생겨버린다.
            이런 경우를 방지하기 위해 1개라도 넘치는 페이지만 다음으로 밀어낸다.
            즉 10개에 5개를 다 더하면 15가 되어 아무것도 없는 3페이지가 생기지만, 4개만 더하면 14가 되어 
            여전히 2페이지에 머문다.
        """
        return (self.total_items + self.limit - 1) // self.limit

class PaginatedResponse(BaseModel,Generic[T]):
    content: list[T] = Field(...,description="데이터 리스트")
    pagination: PaginationMeta
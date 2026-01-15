from typing import Generic, Optional,TypeVar
from pydantic import BaseModel
# responseBody 응답시 응답의 형식을 지정하는 공통함수
T = TypeVar("T")

#제네릭을 사용한 이유는 하나의 공통 응답 틀을 유지하면서도,
#그 내부의 데이터(data)는 유저, 게시글 등 어떤 타입이든 안전하게 담기 위해서
class CommonResponse(Generic[T],BaseModel):
    status: str = "success"
    message: str = "요청이 성공적으로 처리되었습니다."
    data: Optional[T] = None
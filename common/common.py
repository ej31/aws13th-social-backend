from typing import Generic, Optional,TypeVar
from pydantic import BaseModel
# responseBody 응답시 응답의 형식을 지정하는 공통함수
T = TypeVar("T")

class CommonResponse(BaseModel, Generic[T]):
    status: str = "success"
    messages: str = "요청이 성공적으로 처리되었습니다."
    data: Optional[T] = None
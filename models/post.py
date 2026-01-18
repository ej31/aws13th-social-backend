from typing import Optional, Annotated
from fastapi.params import Form
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    media : Optional[HttpUrl] = None

def post_form_reader(
        title : Annotated[str, Form(...)],
        content : Annotated[str, Form(...)],
        media : Optional[Annotated[str, Form(...)]] = None,
) -> Post:
    return Post(
        title = title,
        content = content,
        media = media,
    )

class PostInternal(BaseModel):
    user_id: str
    post_id: str
    view_count :int
    title: str
    content: str
    media: Optional[HttpUrl] = None
    created_at: datetime

class PostPublic(BaseModel):
    title: str
    content: str
    media : Optional[HttpUrl]

class PostQuery(BaseModel):
    page: int = Field(1,ge=1, description="페이지 번호 1번부터 시작")
    size : int = Field(10, ge=1, le=100, description="페이지 개수, 총 100")
    search : Optional[str] = Field(None,min_length=2, max_length=100)
    sort_by : str= Field("created_at",description="정렬 기준 필드")
    sort_order : str= Field("desc",description="정렬 방향 오름차순")

    @property
    def start_idx(self) -> int:
        return (self.page - 1) * self.size

    @property
    def end_idx(self) -> int:
        return self.page * self.size


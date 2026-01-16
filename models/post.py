from typing import Optional, Annotated

from fastapi.params import Form
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    media : Optional[HttpUrl] = None
    created_at: datetime

def post_form_reader(
        title : Annotated[str, Form(...)],
        content : Annotated[str, Form(...)],
        media : Optional[Annotated[str, Form(...)]] = None,
        created_at: datetime = datetime.now()
) -> Post:
    return Post(
        title = title,
        content = content,
        media = media,
        created_at = created_at
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


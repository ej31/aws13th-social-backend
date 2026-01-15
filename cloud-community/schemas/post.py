from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    author_id: int


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class Post(PostBase):
    id: int
    author_id: int


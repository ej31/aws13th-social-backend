from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    post_id: int
    user_id: int


class CommentUpdate(BaseModel):
    content: str | None = None


class Comment(CommentBase):
    id: int
    post_id: int
    user_id: int

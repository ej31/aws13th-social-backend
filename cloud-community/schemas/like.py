from pydantic import BaseModel


class LikeBase(BaseModel):
    post_id: int
    user_id: int


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int


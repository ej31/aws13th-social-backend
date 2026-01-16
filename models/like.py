from pydantic import BaseModel


class Like(BaseModel):
    is_like: bool

class LikesResponse(BaseModel):
    is_like: bool
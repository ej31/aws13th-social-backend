from pydantic import BaseModel

class Pagination(BaseModel):
    page: int
    limit: int
    total: int

class FailResponse(BaseModel):
    status: str
    message: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
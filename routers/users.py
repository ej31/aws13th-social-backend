
from fastapi import APIRouter

from schemas.post import PostOut
from schemas.user import UserOut


router = APIRouter(
    prefix="/users",
    tags=["users"]
)
@router.get("/me",response_model=UserOut)
def getprofile(payload: UserOut):
    pass

@router.get("/me/posts/likes/summary",response_model=PostOut)
def get_total_likes(payload: UserOut):
    pass
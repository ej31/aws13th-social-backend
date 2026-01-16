from fastapi import APIRouter
from schemas.post import PostCreate

router = APIRouter()

@router.post("/")
def create_post(post: PostCreate):
    return{
        "message": "게시글 작성 성공",
        "data": post
    }
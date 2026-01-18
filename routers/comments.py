from fastapi import APIRouter
from schemas.comment import CommentCreate

router = APIRouter()

@router.post("/")
def create_comment(post_id: int, comment: CommentCreate):
    return {"message": f"{post_id}번 글에 댓글 작성", "data": comment}

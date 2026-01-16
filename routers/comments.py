from fastapi import APIRouter
from schemas.comment import CommentCreate

router = APIRouter()

@router.post("/{postId}/comments")
def create_comment(postId: int, comment: CommentCreate):
    return {"message": f"{postId}번 글에 댓글 작성", "data": comment}

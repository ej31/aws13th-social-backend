# app/routers/comments.py

from fastapi import APIRouter


router = APIRouter(prefix="/posts", tags=["comments"])

# 댓글 목록 조회
@router.get("/{post_id}/comments")
def list_comments():
    pass

# 댓글 작성
@router.post("/{post_id}/comments")
def create_comment():
    pass

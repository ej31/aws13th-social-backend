# app/routers/comments.py
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status

from schemas.comment import CommentCreate, CommentOut
from utils.data import read_json, write_json, next_id
from utils.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["comments"])

# 댓글 목록 조회
@router.get("/{post_id}/comments", response_model=list[CommentOut])
def list_comments(post_id: int):
    comments = read_json("comments.json", default=[])
    return [c for c in comments if int(c["post_id"]) == post_id]

# 댓글 작성
@router.post("/{post_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(post_id: int, payload: CommentCreate, user=Depends(get_current_user)):
    posts = read_json("posts.json", default=[])
    if not any(int(p["id"]) == post_id for p in posts):
        raise HTTPException(status_code=404, detail="POST_NOT_FOUND")

    comments = read_json("comments.json", default=[])
    comment = {
        "id": next_id(comments),
        "post_id": post_id,
        "author_id": int(user["id"]),
        "comment": payload.comment,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    comments.append(comment)
    write_json("comments.json", comments)
    return comment

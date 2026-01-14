from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status

from schemas.comment import CommentResponse, CommentCreate
from utils import data, auth

router = APIRouter(
    prefix="/posts/{post_id}/comments",
    tags=["comments"]
)

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
        post_id: int,
        comment: CommentCreate,
        current_user: dict = Depends(auth.get_current_user)
):
    comment_post = data.find_by_id("posts.json", post_id)
    if not comment_post:
        raise HTTPException(status_code=404, detail="해당 게시물 존재하지 않음")

    comment_id = data.get_next_id("comments.json")
    now = datetime.now(timezone.utc).isoformat()
    new_comment = {
        "id": comment_id,
        "post_id": post_id,
        "user_id": current_user["id"],
        "author_nickname": current_user["nickname"],
        "content": comment.content,
        "created_at": now,
        "updated_at": now
    }

    comments = data.load_data("comments.json")
    comments.append(new_comment)
    success = data.save_data(comments, "comments.json")
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="댓글 데이터 저장 실패"
        )
    return CommentResponse(
        id=comment_id,
        post_id=post_id,
        user_id=current_user["id"],
        author_nickname=current_user["nickname"],
        content=comment.content,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )


@router.get("/", response_model=List[CommentResponse], status_code=status.HTTP_200_OK)
async def get_comments_by_post(post_id: int):
    post = data.find_by_id("posts.json", post_id)
    if not post:
        raise HTTPException(status_code=404, detail="해당 게시물 존재하지 않음")

    comments = data.load_data("comments.json")
    post_comments = [c for c in comments if c.get("post_id") == post_id]

    return [
        CommentResponse(
            id=c["id"],
            post_id=c["post_id"],
            user_id=c["user_id"],
            author_nickname=c["author_nickname"],
            content=c["content"],
            created_at=c["created_at"],
            updated_at=c["updated_at"]
        )
        for c in post_comments
    ]

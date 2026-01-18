from typing import Annotated
from fastapi import APIRouter, Depends
from dependencies.auth import get_current_user
from models.comment import Comment, CommentResponse
from services.comments_service import write_comments

router = APIRouter(tags=["comments"])

@router.post("/posts/{post_id}/comments")
def post_comments(
        post_id: str,
        comment_data: Annotated[Comment, Depends(Comment)],
        current_user: Annotated[dict, Depends(get_current_user)]

):
    return write_comments(post_id, comment_data, current_user)


@router.get("posts/{post_id}/comments",response_model=CommentResponse)
def get_comments(
        post_id: str,
        comment_data : Annotated[Comment, Depends(Comment)],
        current_user: Annotated[dict, Depends(get_current_user)]
):
    return write_comments(post_id,comment_data,current_user)


@router.patch("/comments/{comment_id}")
def update_comments(comment_id: int):
    return comment_id

@router.delete("/comments/{comment_id}")
def delete_comments(comment_id: int):
    return comment_id

@router.get("/comments/me")
def get_me():
    return get_me()

from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user, get_optional_user
from models.comment import Comment, CommentResponse, AllComments
from services.comments_service import write_comments, get_usr_comments, update_user_comments, delete_user_comments, \
    get_my_comment

router = APIRouter(tags=["comments"])

@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
def post_comments(
        post_id: str,
        comment_data: Annotated[Comment, Depends(Comment)],
        current_user: Annotated[dict, Depends(get_current_user)]
):
    return write_comments(post_id, comment_data, current_user)

@router.get("/posts/{post_id}/comments", response_model=AllComments)
def get_comments(
        post_id: str,
        current_user: Annotated[dict, Depends(get_optional_user)]
):
    all_comment = get_usr_comments(post_id,current_user)

    return {
        "total": len(all_comment),
        "comments": all_comment
    }

@router.patch("/comments/{comment_id}", response_model=CommentResponse)
def update_comments(
        comment_id: str,
        comment_data: Annotated[Comment, Depends(Comment)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    return update_user_comments(comment_id, comment_data, current_user)

@router.delete("/comments/{comment_id}", response_model=CommentResponse)
def delete_comments(
        comment_id: str,
        current_user: Annotated[dict, Depends(get_current_user)],):
    delete_user_comments(comment_id, current_user)
    return {"comment": "코멘트가 삭제 되었습니다."}

@router.get("/comments/me")
def get_me(
        current_user: Annotated[dict, Depends(get_current_user)],
):
    return get_my_comment(current_user)

from fastapi import APIRouter, Depends
from typing import Annotated
from models.like import LikeResponse, LikeCreate
from services.likes_service import toggle_like_service
from dependencies.auth import get_current_user

router = APIRouter(tags=["likes"])

@router.post("/likes", response_model=LikeResponse)
def toggle_like(
    like_in: LikeCreate,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return toggle_like_service(current_user["user_id"], like_in)


@router.post("/posts/{post_id}/likes", response_model=LikeResponse)
def like_post(post_id: str,
              current_user: Annotated[dict, Depends(get_current_user)]
    ):
    user_id = current_user["user_id"]
    like_in = LikeCreate(target_type="PostLike", target_id=post_id)
    return toggle_like_service(user_id,like_in)


@router.post("/comments/{comment_id}/likes", response_model=LikeResponse)
def like_comment(
    comment_id: str,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    user_id = current_user["user_id"]
    like_in = LikeCreate(target_type="CommentLike", target_id=comment_id)
    return toggle_like_service(user_id, like_in)

# @router.get("/likes/me")
# def like_me(current_user: Annotated[dict, Depends(get_current_user)]):
#     return get_my_likes(current_user)
#
# @router.get("posts/{post_id}/likes", response_model=LikesResponsePost)
# def like_post(post_id: str,current_user: Annotated[dict, Depends(get_current_user)]):
#     return get_like_post(post_id,current_user)
#
# @router.get("/comments/{comment_id}/likes", response_model=LikesResponseComment)
# def like_comment(comment_id: str,current_user: Annotated[dict, Depends(get_current_user)]):
#     return get_like_comment(comment_id,current_user)
#
# @router.delete("/posts/{post_id}/likes", response_model=LikesResponsePost)
# def like_post(post_id: str, current_user: Annotated[dict, Depends(get_current_user)]):
#     return delete_post_commet(post_id,current_user)
#
# @router.delete("/comments/{comment_id}/likes", response_model=LikesResponseComment)
# def like_comment(comment_id: str, current_user: Annotated[dict, Depends(get_current_user)]):
#     return delete_like_comment(comment_id,current_user)
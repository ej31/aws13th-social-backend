from fastapi import APIRouter, Depends, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from models.auth import UserSignUp, UserLogin, UserUpdate
from models.like import LikeResponse, LikeCreate
from models.user import AuthResponse, UserPublic
from services.auth_service import signup_user, login_user
from services.likes_service import write_like_post, write_like_comment, get_my_likes, delete_like_comment, \
    delete_post_commet, get_like_comment, get_like_post, toggle_like_service
from services.user_service import get_my_profile,get_user_profile,update_my_profile,delete_my_account
from dependencies.auth import get_current_user
from datetime import datetime, timezone

router = APIRouter(tags=["likes"])

@router.post("/likes", response_model=LikeResponse)
def toggle_like(
    like_in: LikeCreate,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return toggle_like_service(current_user["user_id"], like_in)

#
# @router.post("/posts/{post_id}/likes", response_model=LikesResponsePost)
# def like_post(post_id: str,
#               current_user: Annotated[dict, Depends(get_current_user)]
#     ):
#     return write_like_post(post_id,current_user)
#
# @router.post("/comments/{comment_id}/likes", response_model=LikesResponseComment)
# def like_comment(
#     comment_id: str,
#     current_user: Annotated[dict, Depends(get_current_user)]
# ):
#     return write_like_comment(comment_id,current_user)
#
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
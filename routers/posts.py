from typing import Annotated
from fastapi import APIRouter, Depends
from dependencies.auth import get_current_user
from models.post import PostPublic, Post, post_form_reader
from services.post_service import write_posts, get_user_post, update_my_post, delete_my_post

router = APIRouter(tags=["posts"])

@router.post("/posts", response_model=PostPublic)
async def create_post(
        post_data:Annotated[Post, Depends(post_form_reader)],
        current_user : Annotated[dict,Depends(get_current_user)]
):
    # post_dict = post_data.model_dump(exclude_unset=True,mode="json")
    return write_posts(post_data, current_user)

@router.get("/posts/{post_id}",response_model=PostPublic)
async def get_post(post_id: str):
    return get_user_post(post_id)

@router.patch("/posts/{post_id}")
async def update_post(
        post_id:str,
        post_data: Annotated[Post, Depends(post_form_reader)],
        current_user: Annotated[dict, Depends(get_current_user)]
):
    post_dict = post_data.model_dump(exclude_unset=True, mode="json")
    return update_my_post(post_id,post_dict, current_user)

@router.delete("/posts/{post_id}")
async def delete_post(
        post_id:str,
        current_user: Annotated[dict, Depends(get_current_user)] ):
    delete_my_post(post_id,current_user)
    return {"post_id": "삭제 되었습니다."}


from fastapi import APIRouter, FastAPI, HTTPException, Depends, status
from app.schemas.posts import PostCreateRequest, PostUpdateRequest
from typing import Annotated
from app.dependencies.auth import get_current_user
from app.utils.data import read_posts, write_posts, read_users
from datetime import datetime, timezone
import uuid

router = APIRouter(prefix="/posts",tags=["posts"])

@router.post("/", summary="게시글 작성", description="사용자가 게시글의 제목과 내용을 입력하고 게시글을 작성하는 리소스(로그인 필요)", tags=["posts"])
async def create_post(new_post: PostCreateRequest, current_user: Annotated[dict, Depends(get_current_user)]):
    posts = read_posts()

    post = {
        "id": str(uuid.uuid4()),
        "title": new_post.title,
        "content": new_post.content,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "author": {
            "id": current_user.get("id"),
            "nickname": current_user.get("nickname"),
            "profile_image": current_user.get("profile_image"),
        }
    }

    posts.append(post)
    write_posts(posts)

    return {"data" :post}

@router.patch("/{post_id}", summary="게시글 수정", description="본인이 작성한 글의 제목과 내용을 수정할 수 있습니다.(로그인 필요)", tags=["posts"])
async def patch_post(post_id:str, change_posts: PostUpdateRequest, current_user: Annotated[dict, Depends(get_current_user)],):
    posts = read_posts()

    post_idx = None
    for i,p in enumerate(posts):
        if p["id"] == post_id:
            post_idx = i
            break

    if post_idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다."
        )
    if current_user.get("id") != posts[post_idx]["author"]["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인이 작성한 게시물만 수정할 수 있습니다."
        )

    if change_posts.title is not None:
        posts[post_idx]["title"] = change_posts.title

    if change_posts.content is not None:
        posts[post_idx]["content"] = change_posts.content

    write_posts(posts)

    return{"status": "success","message": "게시물 수정이 완료되었습니다.","data": posts[post_idx]}

@router.delete("/{post_id}", summary="게시글 삭제",description="본인이 작성한 게시글을 삭제하는 리소스", tags=["posts"])
async def delete_post(post_id: str, current_user: Annotated[dict, Depends(get_current_user)],):
    posts = read_posts()

    post_idx = None
    for i,p in enumerate(posts):
        if p["id"] == post_id:
            post_idx = i
            break

    if post_idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다."
        )

    if current_user.get("id") != posts[post_idx]["author"]["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인이 작성한 게시물만 삭제할 수 있습니다."
        )
    posts[post_idx]["is_deleted"] = True

    return{"status": "success", "message": "게시물 삭제가 완료되었습니다."}

@router.get("/", summary="게시글 목록 조회",description= "게시글 목록을 조회합니다(페이지네이션 적용)", tags=["posts"])
async def get_posts():
    return

@router.get("/search", summary="게시글 검색",description= "keyword를 통해 게시글 검색하는 리소스", tags=["posts"])
async def get_posts_by_keywords(keyword: str):
    return

@router.get("/sort", summary="게시물 정렬",description= "게시물을 최신순, 조회수순, 좋아요순 등으로 정렬하는 리소스.", tags=["posts"])
async def sort_posts():
    return

@router.get("/{post_id}", summary="게시글 상세 조회",description= "게시글의 id값을 통해 게시글을 상세 조회하는 리소스.", tags=["posts"])
async def get_posts_by_id(post_id: int):
    return



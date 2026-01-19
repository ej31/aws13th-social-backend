from ast import keyword
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from fastapi import Depends

from schemas.post import PostOut, PostCreate, PostUpdate
from utils.auth import get_current_user
from utils.data import read_json, next_id, write_json

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

# 게시글 목록 조회 (페이지네이션 추가하기)
@router.get("/", response_model=list[PostOut])
def list_post():
    return read_json("posts.json",default=[])

# 게시글 검색
@router.get("/",response_model=PostOut)
def search_post(query=keyword):
    posts = read_json("posts.json",default=[])
    pass

# 게시글 상세 조회
@router.get("/{post_id}",response_model=PostOut)
def get_post(post_id: int, user=Depends(get_current_user)):
    posts = read_json("posts.json",default=[])
    pass

# 게시글 작성
@router.post("/",response_model=PostOut)
def create_post(payload: PostCreate, user=Depends(get_current_user)):
    posts = read_json("posts.json",default=[])
    post = {
        "id": next_id(posts),
        "title": payload.title,
        "content": payload.content,
        "author_id": int(user["id"]),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    posts.append(post)
    read_json("posts.json",default=posts)
    return posts

# 게시글 수정
@router.patch("/{post_id}",response_model=PostOut)
def update_post(post_id: int, payload: PostUpdate, user=Depends(get_current_user)):
    posts = read_json("posts.json",default=[])
    post = next((p for p in posts if int(p["id"]) == int(post_id)), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if not(post["author_id"] == int(user["id"])):
        raise HTTPException(status_code=403, detail="User doesn't have permission")
    if payload.title is not None:
        post["title"] = payload.title
    if payload.content is not None:
        post["content"] = payload.content
    write_json("posts.json",posts)
    return post

# 게시글 삭제
@router.delete("/{post_id}")
def delete_post(post_id: int, user=Depends(get_current_user)):
    posts = read_json("posts.json",default=[])
    post = next((p for p in posts if int(p["id"]) == post_id),None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if not(post["author_id"] == int(user["id"])):
        raise HTTPException(status_code=403, detail="User doesn't have permission")
    posts = [p for p in posts if int(p["id"]) is not post_id]
    write_json("posts.json",posts)
    return {"message": "success"}

# 게시글 정렬

# 내가 쓴 게시글 목록
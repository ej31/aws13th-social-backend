from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query

from schemas.like import LikeOut
from schemas.post import PostLikedOut
from utils.auth import get_current_user
from utils.data import read_json, write_json, next_id

from datetime import datetime


router = APIRouter(prefix="", tags=["likes"])

def _parse_dt(dt: Optional[str]) -> Optional[datetime]:
    # from/to가 들어오면 ISO8601(date-time)로 파싱.
    if not dt:
        return None
    try:
        return datetime.fromisoformat(dt)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date-time format (ISO8601 required)")


def _post_in_range(post: dict, from_dt: Optional[datetime], to_dt: Optional[datetime]) -> bool:

    # posts.json에 created_at이 있으면 범위 필터 적용.
    # 없으면 범위 조건 무시하고 포함 처리.

    if not from_dt and not to_dt:
        return True

    created_at = post.get("created_at")
    if not created_at:
        # created_at이 없으면 범위 필터를 정확히 할 수 없으니 "포함"으로 처리(혹은 제외로 처리해도 됨)
        return True

    try:
        created = datetime.fromisoformat(created_at)
    except ValueError:
        return True

    if from_dt and created < from_dt:
        return False
    if to_dt and created > to_dt:
        return False
    return True

# 좋아요 등록
@router.post("/posts/{postId}/likes", status_code=201)
def like_post(post_id: int, user=Depends(get_current_user)):
    posts = read_json("posts.json", default=[])
    if not any(int(p["id"]) == post_id for p in posts):
        raise HTTPException(status_code=404, detail="POST_NOT_FOUND")
    likes = read_json("likes.json", default=[])
    # 이미 좋아요 눌렀으면 200으로 멱등 처리
    existing = next(
        (l for l in likes if int(l["post_id"]) == post_id and int(l["user_id"]) == int(user["id"])),
        None,
    )
    if existing:
        return {"status": "success"}

    likes.append({"id": next_id(likes), "post_id": post_id, "user_id": int(user["id"])})
    write_json("likes.json", likes)
    return {"status": "success"}

# 좋아요 취소
@router.delete("/posts/{postId}/likes", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(post_id: int, user=Depends(get_current_user)):
    posts = read_json("posts.json", default=[])
    if not any(int(p["id"]) == post_id for p in posts):
        raise HTTPException(status_code=404, detail="POST_NOT_FOUND")
    likes = read_json("likes.json", default=[])
    before = len(likes)
    likes = [
        l for l in likes
        if not (int(l["post_id"]) == post_id and int(l["user_id"]) == int(user["id"]))
    ]
    if len(likes) == before:
        # 취소할 좋아요가 없어도 204로 멱등 처리
        write_json("likes.json", likes)  # 없어도 됨
        return
    write_json("likes.json", likes)
    return

# 좋아요 상태 확인
@router.get("/users/me/posts/likes/summary", response_model=LikeOut)
def my_likes_summary(
    from_: Optional[str] = None,
    to: Optional[str] = None,
    user=Depends(get_current_user)
):
    from_dt = _parse_dt(from_)
    to_dt = _parse_dt(to)

    posts = read_json("posts.json", default=[])
    likes = read_json("likes.json", default=[])

    # 기간 필터된 게시글 id들
    filtered_post_ids = {int(p["id"]) for p in posts if _post_in_range(p, from_dt, to_dt)}

    # (내가 받은 좋아요) = 내 게시글들에 달린 좋아요 총합
    my_post_ids = {int(p["id"]) for p in posts if int(p.get("author_id", -1)) == int(user["id"])}
    my_post_ids = my_post_ids & filtered_post_ids

    total_like_count = sum(1 for l in likes if int(l["post_id"]) in my_post_ids)
    has_any_like = total_like_count > 0
    post_count = len(my_post_ids)

    return {
        "has_any_like": has_any_like,
        "total_like_count": total_like_count,
        "post_count": post_count,
    }

# 내가 좋아요한 게시글 목록
@router.get("/users/me/likes", response_model=list[PostLikedOut])
def my_liked_posts(
    page: int = Query(1, ge=1, description="페이지 번호(1부터)"),
    size: int = Query(10, ge=1, le=20, description="페이지당 개수(1~20)"),
    sort: str = Query("created_at", pattern="^(created_at|like_count)$", description="정렬 기준(created_at|like_count)"),
    order: str = Query("desc", pattern="^(asc|desc)$", description="정렬 방향(asc|desc)"),
    user=Depends(get_current_user),
):
    posts = read_json("posts.json", default=[])
    likes = read_json("likes.json", default=[])

    my_user_id = int(user["id"])

    # 1) 내가 좋아요한 post_id 모으기
    liked_post_ids = {int(l["post_id"]) for l in likes if int(l["user_id"]) == my_user_id}

    # 2) post_id -> like_count 계산(전체 likes에서 집계)
    like_count_map: dict[int, int] = {}
    for l in likes:
        pid = int(l["post_id"])
        like_count_map[pid] = like_count_map.get(pid, 0) + 1

    # 3) posts.json에서 해당 게시글만 뽑아서 응답 형태로 변환
    liked_posts: list[dict] = []
    for p in posts:
        pid = int(p["id"])
        if pid in liked_post_ids:
            liked_posts.append({
                "id": pid,
                "title": p.get("title", ""),
                "content": p.get("content", ""),
                "author_id": int(p.get("author_id", 0)),
                "created_at": p.get("created_at"),
                "like_count": like_count_map.get(pid, 0),
            })

    # 4) 정렬
    reverse = (order == "desc")

    if sort == "like_count":
        liked_posts.sort(key=lambda x: x["like_count"], reverse=reverse)
    else:
        # created_at이 없으면 None이 되어 정렬이 깨질 수 있으니 문자열 기본값 처리
        liked_posts.sort(key=lambda x: x["created_at"] or "", reverse=reverse)
    start = (page - 1) * size
    end = start + size
    return liked_posts[start:end]

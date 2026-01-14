from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.post import PostResponse, PostCreate
from utils import auth, data

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_new_post(
        post_data: PostCreate,
        current_user: dict = Depends(auth.get_current_user)
):
    post_id = data.get_next_id("posts.json")
    now = datetime.now(timezone.utc).isoformat()
    new_post = {
        "id": post_id,
        "user_id": current_user["id"],
        "author_nickname": current_user["nickname"],
        "title": post_data.title,
        "content": post_data.content,
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
        "created_at": now,
        "updated_at": now
    }

    posts = data.load_data("posts.json")
    posts.append(new_post)
    success = data.save_data(posts, "posts.json")
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="게시글 데이터 저장 실패"
        )

    return PostResponse(
        id=new_post["id"],
        user_id=new_post["user_id"],
        author_nickname=new_post["author_nickname"],
        title=new_post["title"],
        content=new_post["content"],
        view_count=new_post["view_count"],
        like_count=new_post["like_count"],
        comment_count=new_post["comment_count"],
        created_at=new_post["created_at"],
        updated_at=new_post["updated_at"]
    )
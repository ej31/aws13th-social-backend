from datetime import datetime, UTC

from aiomysql import IntegrityError
from fastapi import APIRouter, HTTPException, status

from config import settings
from routers.users import CurrentUserId
from schemas.commons import PostId, Page, Pagination, CurrentCursor
from schemas.like import LikedListItem, ListPostILiked, LikeStatusResponse
from utils.database import read_json, write_json
from utils.pagination import paginate

LIKES_PAGE_SIZE = 20

router = APIRouter(
    tags=["LIKES"],
)


@router.get("/posts/liked", response_model=ListPostILiked)
def get_posts_liked(user_id: CurrentUserId, page: Page = 1) -> ListPostILiked:
    """내가 좋아요한 게시글 목록"""
    likes = read_json(settings.likes_file)
    posts = read_json(settings.posts_file)

    # 내가 좋아요한 post_id 목록 (최신순 정렬)
    my_likes = sorted((like for like in likes if like['user_id'] == user_id), key=lambda like: like['created_at'], reverse=True)
    liked_post_ids = [like["post_id"] for like in my_likes]

    # 좋아요한 게시글 정보 가져오기 (좋아요 순서 유지)
    posts_dict = {post["id"]: post for post in posts}
    liked_posts = [
        posts_dict[post_id] for post_id in liked_post_ids
        if post_id in posts_dict
    ]

    paginated_posts, actual_page, total_pages = paginate(liked_posts, page, LIKES_PAGE_SIZE)

    return ListPostILiked(
        data=[LikedListItem(
            post_id=post["id"],
            author=post["author"],
            title=post["title"],
            view_count=post.get("view_count", 0),
            like_count=post.get("like_count", 0),
            created_at=post["created_at"]
        ) for post in paginated_posts],
        pagination=Pagination(page=actual_page, total=total_pages)
    )


@router.post("/posts/{post_id}/likes", response_model=LikeStatusResponse,
             status_code=status.HTTP_201_CREATED)
async def create_like(post_id: PostId, user_id: CurrentUserId, cur: CurrentCursor) -> LikeStatusResponse:
    """좋아요 등록"""
    # 게시글 존재 확인
    await cur.execute("SELECT id FROM posts WHERE id = %s", (post_id,))
    if not await cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # 좋아요 등록 (복합 PK이므로 중복 시 IntegrityError)
    now = datetime.now(UTC)
    try:
        await cur.execute(
            "INSERT INTO likes (post_id, user_id, created_at) VALUES (%(post_id)s, %(user_id)s, %(created_at)s)",
            {
                "post_id": post_id,
                "user_id": user_id,
                "created_at":now
            }
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already liked"
        )

    # 트리거가 like_count 자동 증가
    await cur.execute("SELECT like_count FROM posts WHERE id = %s", (post_id,))
    post = await cur.fetchone()

    return LikeStatusResponse(
        liked=True,
        like_count=post["like_count"] if post else 1,
    )


@router.delete("/posts/{post_id}/likes", response_model=LikeStatusResponse)
async def delete_like(post_id: PostId, user_id: CurrentUserId, cur: CurrentCursor) -> LikeStatusResponse:
    """좋아요 취소"""
    await cur.execute(
        "DELETE FROM likes WHERE post_id = %s AND user_id = %s",
        (post_id, user_id)
    )

    if cur.rowcount == 0:
        await cur.execute("SELECT id FROM posts WHERE id = %s", (post_id,))
        if not await cur.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Like not found"
        )

    # 트리거가 like_count 자동 감소
    await cur.execute("SELECT like_count FROM posts WHERE id = %s", (post_id,))
    post = await cur.fetchone()

    return LikeStatusResponse(
        liked=False,
        like_count=post["like_count"] if post else 0,
    )



@router.get("/posts/{post_id}/likes", response_model=LikeStatusResponse)
async def get_like_status(post_id: PostId, user_id: CurrentUserId, cur: CurrentCursor) -> LikeStatusResponse:
    """좋아요 상태 확인"""
    await cur.execute("SELECT like_count FROM posts WHERE id = %s", (post_id,))
    post = await cur.fetchone()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # 좋아요 여부 확인
    await cur.execute(
        "SELECT 1 FROM likes WHERE post_id = %s AND user_id = %s",
        (post_id, user_id)
    )
    is_liked = await cur.fetchone() is not None

    return LikeStatusResponse(
        liked=is_liked,
        like_count=post["like_count"]
    )

import uuid

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.models.like import Like
from db.models.post import Post
from routers.users import CurrentUserId
from schemas.commons import PostId, Page, Pagination, CurrentCursor, DBSession
from schemas.like import LikeStatusResponse, LikedPostsResponse
from schemas.post import PostListItem

LIKES_PAGE_SIZE = 20

router = APIRouter(
    tags=["LIKES"],
)

async def _get_post_or_404(db: DBSession, post_id: PostId) -> Post:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post

@router.get("/posts/liked", response_model=LikedPostsResponse)
async def get_posts_liked(user_id: CurrentUserId, cur: CurrentCursor, page: Page = 1) -> LikedPostsResponse:
    """내가 좋아요한 게시글 목록"""
    offset = (page - 1) * LIKES_PAGE_SIZE

    # 총 개수 조회
    await cur.execute(
        "SELECT COUNT(*) as total FROM likes WHERE user_id = %s",
        (user_id,)
    )
    total_count = (await cur.fetchone())["total"]
    total_pages = (total_count + LIKES_PAGE_SIZE - 1) // LIKES_PAGE_SIZE or 1

    await cur.execute(
        """
        SELECT p.id as post_id, p.author_id as author, p.title, p.view_count, p.like_count, p.created_at
        FROM likes l
        JOIN posts p ON l.post_id = p.id
        WHERE l.user_id = %s
        ORDER BY l.created_at DESC
        LIMIT %s OFFSET %s
        """,
        (user_id, LIKES_PAGE_SIZE, offset)
    )
    liked_posts = await cur.fetchall()

    return LikedPostsResponse(
        data=[PostListItem(**post) for post in liked_posts],
        pagination=Pagination(page=page, total=total_pages)
    )


@router.post("/posts/{post_id}/likes", response_model=LikeStatusResponse,
             status_code=status.HTTP_201_CREATED)
async def create_like(post_id: PostId, user_id: CurrentUserId, db: DBSession) -> LikeStatusResponse:
    """좋아요 등록"""
    post = await _get_post_or_404(db, post_id)

    new_like = Like(
        id=f"like_{uuid.uuid4().hex}",
        post_id=post_id,
        user_id=user_id
    )
    db.add(new_like)

    try:
        await db.flush()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already liked"
        )
    # 트리거가 like_count 자동 증가
    await db.refresh(post)
    return LikeStatusResponse(
        liked=True,
        like_count=post.like_count,
    )


@router.delete("/posts/{post_id}/likes", response_model=LikeStatusResponse)
async def delete_like(post_id: PostId, user_id: CurrentUserId, db: DBSession) -> LikeStatusResponse:
    """좋아요 취소"""
    post = await _get_post_or_404(db, post_id)
    result = await db.execute(
        select(Like)
        .where(Like.post_id == post_id, Like.user_id == user_id)
    )
    like = result.scalar_one_or_none()
    if like is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Like not found"
        )

    await db.delete(like)
    await db.flush()
    await db.refresh(post)  # 트리거가 like_count 감소 → 최신값 가져오기

    return LikeStatusResponse(
        liked=False,
        like_count=post.like_count
    )


@router.get("/posts/{post_id}/likes", response_model=LikeStatusResponse)
async def get_like_status(post_id: PostId, user_id: CurrentUserId, db: DBSession) -> LikeStatusResponse:
    """좋아요 상태 확인"""
    # 게시글 조회
    post_result = await db.execute(select(Post).where(Post.id == post_id))
    post = post_result.scalar_one_or_none()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # 좋아요 여부 확인
    like_result = await db.execute(
        select(Like).where(Like.post_id == post_id, Like.user_id == user_id)
    )
    is_liked = like_result.scalar_one_or_none() is not None

    return LikeStatusResponse(
        liked=is_liked,
        like_count=post.like_count,
    )

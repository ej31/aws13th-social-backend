"""
좋아요 API
- 좋아요 등록
- 좋아요 취소
- 좋아요 상태 확인
- 내가 좋아요한 게시글 목록
"""
from fastapi import APIRouter, HTTPException, status, Query
from math import ceil

from app.schemas.like import LikeResponse, LikeStatusResponse
from app.schemas.post import PostResponse, PostAuthorInfo
from app.schemas.common import APIResponse, PaginationResponse
from app.api.deps import CurrentUser, CurrentUserOptional, LikeRepo, PostRepo

router = APIRouter()


@router.post(
    "/posts/{post_id}/likes",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse[LikeResponse]
)
def create_like(
    post_id: int,
    current_user: CurrentUser,
    like_repo: LikeRepo = None,
    post_repo: PostRepo = None
):
    """
    좋아요 등록
    """
    # 게시글 존재 확인
    post = post_repo.find_by_post_id(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 중복 체크
    if like_repo.is_liked(post_id, current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 좋아요를 누른 게시글입니다"
        )
    
    # 좋아요 생성
    like = like_repo.create_like(post_id, current_user["user_id"])
    
    # 게시글 좋아요 수 증가
    post_repo.increment_likes(post_id)
    
    # 응답
    like_response = LikeResponse(
        post_id=like["post_id"],
        user_id=like["user_id"],
        created_at=like["created_at"]
    )
    
    return APIResponse(
        status="success",
        data=like_response
    )


@router.delete("/posts/{post_id}/likes", status_code=status.HTTP_204_NO_CONTENT)
def delete_like(
    post_id: int,
    current_user: CurrentUser,
    like_repo: LikeRepo = None,
    post_repo: PostRepo = None
):
    """
    좋아요 취소
    """
    # 게시글 존재 확인
    post = post_repo.find_by_post_id(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 좋아요 여부 확인
    if not like_repo.is_liked(post_id, current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="좋아요를 누르지 않은 게시글입니다"
        )
    
    # 좋아요 삭제
    success = like_repo.delete_like(post_id, current_user["user_id"])
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="좋아요 취소에 실패했습니다"
        )
    
    # 게시글 좋아요 수 감소
    post_repo.decrement_likes(post_id)
    
    return None


@router.get("/posts/{post_id}/likes/status", response_model=APIResponse[LikeStatusResponse])
def get_like_status(
    post_id: int,
    current_user: CurrentUserOptional = None,
    like_repo: LikeRepo = None,
    post_repo: PostRepo = None
):
    """
    좋아요 상태 확인
    """
    # 게시글 존재 확인
    post = post_repo.find_by_post_id(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 좋아요 수 조회
    total_likes = like_repo.count_by_post_id(post_id)
    
    # 현재 사용자의 좋아요 여부
    is_liked = False
    if current_user:
        is_liked = like_repo.is_liked(post_id, current_user["user_id"])
    
    return APIResponse(
        status="success",
        data=LikeStatusResponse(
            post_id=post_id,
            total_likes=total_likes,
            is_liked=is_liked
        )
    )


@router.get("/users/me/likes", response_model=APIResponse[dict])
def get_my_likes(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: CurrentUser = None,
    like_repo: LikeRepo = None,
    post_repo: PostRepo = None
):
    """
    내가 좋아요한 게시글 목록
    """
    # 내 좋아요 조회
    likes, total = like_repo.find_by_user_id_with_pagination(
        user_id=current_user["user_id"],
        page=page,
        limit=limit
    )
    
    # 게시글 정보 조회
    post_responses = []
    for like in likes:
        post = post_repo.find_by_post_id(like["post_id"])
        if post:  # 게시글이 삭제되지 않은 경우만
            post_responses.append(PostResponse(
                post_id=post["post_id"],
                title=post["title"],
                content=post["content"],
                author=PostAuthorInfo(
                    user_id=post["author_id"],
                    nickname=post["author_nickname"],
                    profile_image=post["author_profile_image"]
                ),
                views=post["views"],
                likes=post["likes"],
                comments_count=post["comments_count"],
                created_at=post["created_at"],
                updated_at=post["updated_at"]
            ))
    
    total_pages = ceil(total / limit) if total > 0 else 0
    
    return APIResponse(
        status="success",
        data={
            "data": post_responses,
            "pagination": PaginationResponse(
                page=page,
                limit=limit,
                total=total,
                total_pages=total_pages
            )
        }
    )
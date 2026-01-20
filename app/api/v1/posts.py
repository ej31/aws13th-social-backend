"""
게시글 API
- 게시글 목록 조회
- 게시글 상세 조회
- 게시글 작성
- 게시글 수정
- 게시글 삭제
"""
from typing import Literal
from fastapi import APIRouter, HTTPException, status, Query
from math import ceil

from app.schemas.post import (
    PostCreateRequest,
    PostUpdateRequest,
    PostResponse,
    PostAuthorInfo
)
from app.schemas.common import APIResponse, PaginationResponse
from app.api.deps import (
    CurrentUser,
    CurrentUserOptional,
    PostRepo,
    CommentRepo,
    LikeRepo
)

router = APIRouter()


@router.get("", response_model=APIResponse[dict])
def get_posts(
    page: int = Query(default=1, ge=1, description="페이지 번호"),
    limit: int = Query(default=20, ge=1, le=100, description="페이지당 항목 수"),
    search: str | None = Query(default=None, description="검색 키워드"),
    sort: Literal["latest", "views", "likes"] = Query(default="latest", description="정렬 기준"),
    post_repo: PostRepo = None
):
    """
    게시글 목록 조회
    """
    # 게시글 조회
    posts, total = post_repo.find_with_pagination(
        page=page,
        limit=limit,
        search=search,
        sort=sort
    )
    
    # 응답 데이터 변환
    post_responses = []
    for post in posts:
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
    
    # 페이지네이션 정보
    safe_total = total if total > 0 else 1
    total_pages = ceil(safe_total / limit)
    
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


@router.get("/{post_id}", response_model=APIResponse[PostResponse])
def get_post(
    post_id: int,
    post_repo: PostRepo = None
):
    """
    게시글 상세 조회
    """
    post = post_repo.find_by_post_id(post_id)
    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 조회수 증가
    post_repo.increment_views(post_id)
    
    # 응답 데이터 구성
    post_response = PostResponse(
        post_id=post["post_id"],
        title=post["title"],
        content=post["content"],
        author=PostAuthorInfo(
            user_id=post["author_id"],
            nickname=post["author_nickname"],
            profile_image=post["author_profile_image"]
        ),
        views=post["views"] + 1,  # 증가된 조회수 반영
        likes=post["likes"],
        comments_count=post["comments_count"],
        created_at=post["created_at"],
        updated_at=post["updated_at"]
    )
    
    return APIResponse(
        status="success",
        data=post_response
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=APIResponse[PostResponse])
def create_post(
    post_data: PostCreateRequest,
    current_user: CurrentUser,
    post_repo: PostRepo = None
):
    """
    게시글 작성
    """
    # 게시글 생성
    post = post_repo.create_post(
        title=post_data.title,
        content=post_data.content,
        author_id=current_user["user_id"],
        author_nickname=current_user["nickname"],
        author_profile_image=current_user["profile_image"]
    )
    
    # 응답 데이터 구성
    post_response = PostResponse(
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
    )
    
    return APIResponse(
        status="success",
        data=post_response
    )


@router.patch("/{post_id}", response_model=APIResponse[PostResponse])
def update_post(
    post_id: int,
    updates: PostUpdateRequest,
    current_user: CurrentUser,
    post_repo: PostRepo = None
):
    """
    게시글 수정
    """
    # 게시글 존재 확인
    post = post_repo.find_by_post_id(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 작성자 확인
    if not post_repo.is_author(post_id, current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인이 작성한 게시글만 수정할 수 있습니다"
        )
    
    # 수정할 데이터 추출
    update_data = updates.model_dump(exclude_none=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="수정할 내용이 없습니다"
        )
    
    # 게시글 수정
    success = post_repo.update_post(post_id, **update_data)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="게시글 수정에 실패했습니다"
        )
    
    # 수정된 게시글 조회
    updated_post = post_repo.find_by_post_id(post_id)
    
    post_response = PostResponse(
        post_id=updated_post["post_id"],
        title=updated_post["title"],
        content=updated_post["content"],
        author=PostAuthorInfo(
            user_id=updated_post["author_id"],
            nickname=updated_post["author_nickname"],
            profile_image=updated_post["author_profile_image"]
        ),
        views=updated_post["views"],
        likes=updated_post["likes"],
        comments_count=updated_post["comments_count"],
        created_at=updated_post["created_at"],
        updated_at=updated_post["updated_at"]
    )
    
    return APIResponse(
        status="success",
        data=post_response
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: CurrentUser,
    post_repo: PostRepo = None,
    comment_repo: CommentRepo = None,
    like_repo: LikeRepo = None
):
    """
    게시글 삭제
    """
    # 게시글 존재 확인
    post = post_repo.find_by_post_id(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 작성자 확인
    if not post_repo.is_author(post_id, current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인이 작성한 게시글만 삭제할 수 있습니다"
        )
    
    # 관련 데이터 삭제
    comment_repo.delete_by_post_id(post_id)  # 댓글 삭제
    like_repo.delete_by_post_id(post_id)      # 좋아요 삭제
    
    # 게시글 삭제
    success = post_repo.delete_post(post_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="게시글 삭제에 실패했습니다"
        )
    
    return None

"""
댓글 API
- 댓글 목록 조회
- 댓글 작성
- 댓글 수정
- 댓글 삭제
- 내가 쓴 댓글 목록
"""
from fastapi import APIRouter, HTTPException, status, Query
from math import ceil

from app.schemas.comment import (
    CommentCreateRequest,
    CommentUpdateRequest,
    CommentResponse
)
from app.schemas.common import APIResponse, PaginationResponse
from app.schemas.user import UserAuthorInfo
from app.api.deps import CurrentUser, CommentRepo, PostRepo

router = APIRouter()


@router.get("/posts/{post_id}/comments", response_model=APIResponse[dict])
def get_comments(
    post_id: int,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    comment_repo: CommentRepo = None,
    post_repo: PostRepo = None
):
    """
    댓글 목록 조회
    """
    # 게시글 존재 확인
    post = post_repo.find_by_post_id(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 댓글 조회
    comments, total = comment_repo.find_by_post_id_with_pagination(
        post_id=post_id,
        page=page,
        limit=limit
    )
    
    # 응답 데이터 변환
    comment_responses = []
    for comment in comments:
        comment_responses.append(CommentResponse(
            comment_id=comment["comment_id"],
            post_id=comment["post_id"],
            content=comment["content"],
            author=UserAuthorInfo(
                user_id=comment["author_id"],
                nickname=comment["author_nickname"],
                profile_image=comment["author_profile_image"]
            ),
            created_at=comment["created_at"],
            updated_at=comment["updated_at"]
        ))
    
    total_pages = ceil(total / limit) if total > 0 else 0
    
    return APIResponse(
        status="success",
        data={
            "data": comment_responses,
            "pagination": PaginationResponse(
                page=page,
                limit=limit,
                total=total,
                total_pages=total_pages
            )
        }
    )


@router.post(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse[CommentResponse]
)
def create_comment(
    post_id: int,
    comment_data: CommentCreateRequest,
    current_user: CurrentUser,
    comment_repo: CommentRepo = None,
    post_repo: PostRepo = None
):
    """
    댓글 작성
    """
    # 게시글 존재 확인
    post = post_repo.find_by_post_id(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 댓글 생성
    comment = comment_repo.create_comment(
        post_id=post_id,
        content=comment_data.content,
        author_id=current_user["user_id"],
        author_nickname=current_user["nickname"],
        author_profile_image=current_user["profile_image"]
    )
    
    # 게시글 댓글 수 증가
    post_repo.increment_comments_count(post_id)
    
    # 응답 데이터 구성
    comment_response = CommentResponse(
        comment_id=comment["comment_id"],
        post_id=comment["post_id"],
        content=comment["content"],
        author=UserAuthorInfo(
            user_id=comment["author_id"],
            nickname=comment["author_nickname"],
            profile_image=comment["author_profile_image"]
        ),
        created_at=comment["created_at"],
        updated_at=comment["updated_at"]
    )
    
    return APIResponse(
        status="success",
        data=comment_response
    )


@router.patch("/comments/{comment_id}", response_model=APIResponse[CommentResponse])
def update_comment(
    comment_id: int,
    updates: CommentUpdateRequest,
    current_user: CurrentUser,
    comment_repo: CommentRepo = None
):
    """
    댓글 수정
    """
    # 댓글 존재 확인
    comment = comment_repo.find_by_comment_id(comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )
    
    # 작성자 확인
    if not comment_repo.is_author(comment_id, current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인이 작성한 댓글만 수정할 수 있습니다"
        )
    
    # 댓글 수정
    success = comment_repo.update_comment(comment_id, updates.content)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="댓글 수정에 실패했습니다"
        )
    
    # 수정된 댓글 조회
    updated_comment = comment_repo.find_by_comment_id(comment_id)
    
    comment_response = CommentResponse(
        comment_id=updated_comment["comment_id"],
        post_id=updated_comment["post_id"],
        content=updated_comment["content"],
        author=UserAuthorInfo(
            user_id=updated_comment["author_id"],
            nickname=updated_comment["author_nickname"],
            profile_image=updated_comment["author_profile_image"]
        ),
        created_at=updated_comment["created_at"],
        updated_at=updated_comment["updated_at"]
    )
    
    return APIResponse(
        status="success",
        data=comment_response
    )


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    current_user: CurrentUser,
    comment_repo: CommentRepo = None,
    post_repo: PostRepo = None
):
    """
    댓글 삭제
    """
    # 댓글 존재 확인
    comment = comment_repo.find_by_comment_id(comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )
    
    # 작성자 확인
    if not comment_repo.is_author(comment_id, current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인이 작성한 댓글만 삭제할 수 있습니다"
        )
    
    post_id = comment["post_id"]
    
    # 댓글 삭제
    success = comment_repo.delete_comment(comment_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="댓글 삭제에 실패했습니다"
        )
    
    # 게시글 댓글 수 감소
    post_repo.decrement_comments_count(post_id)
    
    return None


@router.get("/users/me/comments", response_model=APIResponse[dict])
def get_my_comments(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: CurrentUser = None,
    comment_repo: CommentRepo = None
):
    """
    내가 쓴 댓글 목록
    """
    # 내 댓글 조회
    comments, total = comment_repo.find_by_author_id_with_pagination(
        author_id=current_user["user_id"],
        page=page,
        limit=limit
    )
    
    # 응답 데이터 변환
    comment_responses = []
    for comment in comments:
        comment_responses.append(CommentResponse(
            comment_id=comment["comment_id"],
            post_id=comment["post_id"],
            content=comment["content"],
            author=UserAuthorInfo(
                user_id=comment["author_id"],
                nickname=comment["author_nickname"],
                profile_image=comment["author_profile_image"]
            ),
            created_at=comment["created_at"],
            updated_at=comment["updated_at"]
        ))
    
    total_pages = ceil(total / limit) if total > 0 else 0
    
    return APIResponse(
        status="success",
        data={
            "data": comment_responses,
            "pagination": PaginationResponse(
                page=page,
                limit=limit,
                total=total,
                total_pages=total_pages
            )
        }
    )
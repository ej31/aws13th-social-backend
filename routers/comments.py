from typing import Annotated

from fastapi import APIRouter, status, Depends, Query, Path

from common.dependencies import get_current_user, get_comment_service
from schemas.common_response import CommonResponse
from schemas.pagination import PaginatedResponse, PaginationMeta
from schemas.comment import CommentResponse, CommentCreateRequest, CommentUpdateRequest
from services.comment_service import CommentService
from models.base import User as UserTable  # 타입 힌트용

# 경로 계층 구조를 명확히 하기 위해 접두사를 유지합니다.
router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])


@router.post("/", response_model=CommonResponse[CommentResponse], status_code=status.HTTP_201_CREATED)
async def create_comment(
        post_id: int,
        req: CommentCreateRequest,
        # 1. 이제 dict가 아닌 UserTable 객체를 직접 받습니다.
        current_user: Annotated[UserTable, Depends(get_current_user)],
        # 2. DB 세션이 주입된 get_comment_service를 사용합니다.
        comment_service: Annotated[CommentService, Depends(get_comment_service)]
):
    # 3. 객체 속성(current_user.id)으로 안전하게 접근합니다.
    comment_data = await comment_service.create_comment(post_id, req, current_user.id)

    return CommonResponse(
        status="success",
        message="성공적으로 댓글을 작성하였습니다.",
        data=comment_data
    )


@router.get("/", response_model=CommonResponse[PaginatedResponse[CommentResponse]], status_code=status.HTTP_200_OK)
async def get_comments(
        post_id: int,
        comment_service: Annotated[CommentService, Depends(get_comment_service)],
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100)
):
    comment_data, total_count = await comment_service.get_all_comments(post_id, page, limit)

    paginated_data = PaginatedResponse(
        content=comment_data,
        pagination=PaginationMeta(
            page=page,
            limit=limit,
            total_items=total_count
        )
    )
    return CommonResponse(
        status="success",
        message="성공적으로 댓글 목록을 불러왔습니다.",
        data=paginated_data
    )


@router.patch("/{comment_id}", response_model=CommonResponse[CommentResponse], status_code=status.HTTP_200_OK)
async def update_comment(
        post_id: int,  # 경로 프리픽스에 포함된 post_id를 명시적으로 받습니다.
        comment_id: int,
        req: CommentUpdateRequest,
        current_user: Annotated[UserTable, Depends(get_current_user)],
        comment_service: Annotated[CommentService, Depends(get_comment_service)]
):
    # 서비스 레이어에서 작성자 권한 검증 시 객체의 id를 사용합니다.
    updated_data = await comment_service.update_comment(comment_id, req, current_user.id)

    return CommonResponse(
        status="success",
        message="댓글을 성공적으로 수정하였습니다.",
        data=updated_data
    )


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
        post_id: int,  # 경로 프리픽스에 포함된 post_id
        comment_id: int,
        current_user: Annotated[UserTable, Depends(get_current_user)],
        comment_service: Annotated[CommentService, Depends(get_comment_service)]
):
    await comment_service.delete_comment(comment_id, current_user.id)
    return None
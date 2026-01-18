from typing import Annotated
from fastapi import APIRouter, Depends, status

from schemas.common_response import CommonResponse
from schemas.like import LikeStatusResponse
from services.like_service import LikeService
from common.dependencies import get_current_user

router = APIRouter(prefix="/posts/{post_id}/likes", tags=["likes"])


@router.get("/", response_model=CommonResponse[LikeStatusResponse])
async def get_like_status(
        post_id: int,
        current_user: Annotated[dict, Depends(get_current_user)],
        like_service: Annotated[LikeService, Depends(LikeService)]
):
    """현재 사용자의 좋아요 여부와 게시글의 총 좋아요 수를 조회한다."""
    result = await like_service.get_like_status(post_id, current_user["id"])

    return CommonResponse(
        status="success",
        message="좋아요 상태를 성공적으로 조회했습니다.",
        data=result
    )


@router.post("/", response_model=CommonResponse[LikeStatusResponse])
async def toggle_like(
        post_id: int,
        current_user: Annotated[dict, Depends(get_current_user)],
        like_service: Annotated[LikeService, Depends(LikeService)]
):
    """좋아요를 토글한다. (없으면 등록, 있으면 취소)"""
    result = await like_service.toggle_like(post_id, current_user["id"])

    return CommonResponse(
        status="success",
        message="좋아요 상태가 변경되었습니다.",
        data=result
    )

@router.delete("/", response_model=CommonResponse[None])
async def remove_like(
        post_id: int,
        current_user: Annotated[dict, Depends(get_current_user)],
        like_service: Annotated[LikeService, Depends(LikeService)]
):
    """명시적으로 좋아요를 취소한다."""
    # 이미 좋아요가 있는 경우에만 삭제가 일어나도록 한다..
    await like_service.toggle_like(post_id, current_user["id"])

    return CommonResponse(
        status="success",
        message="좋아요를 취소했습니다.",
        data=None
    )
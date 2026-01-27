from typing import Annotated
from fastapi import APIRouter, status, Depends

from schemas.common_response import CommonResponse
from schemas.like import LikeStatusResponse
from services.like_service import LikeService
from common.dependencies import get_current_user, get_like_service
from models.base import User as UserTable # 타입 힌트용 엔티티

router = APIRouter(prefix="/posts/{post_id}/likes", tags=["likes"])

@router.get("/", response_model=CommonResponse[LikeStatusResponse], status_code=status.HTTP_200_OK)
async def get_like_status(
    post_id: int,
    current_user: Annotated[UserTable, Depends(get_current_user)],
    like_service: Annotated[LikeService, Depends(get_like_service)]
):
    """현재 사용자의 좋아요 여부와 게시글의 총 좋아요 수를 조회한다."""
    result = await like_service.get_like_status(post_id, current_user.id)

    return CommonResponse(
        status="success",
        message="좋아요 상태를 성공적으로 조회했습니다.",
        data=result
    )

@router.post("/", response_model=CommonResponse[LikeStatusResponse], status_code=status.HTTP_201_CREATED)
async def add_like(
    post_id: int,
    current_user: Annotated[UserTable, Depends(get_current_user)],
    like_service: Annotated[LikeService, Depends(get_like_service)]
):
    """좋아요를 등록한다."""
    result = await like_service.add_like(post_id, current_user.id)

    return CommonResponse(
        status="success",
        message="좋아요 상태가 변경되었습니다.",
        data=result
    )

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_like(
    post_id: int,
    current_user: Annotated[UserTable, Depends(get_current_user)],
    like_service: Annotated[LikeService, Depends(get_like_service)]
):
    """명시적으로 좋아요를 취소한다."""
    await like_service.remove_like(post_id, current_user.id)
    return None
from typing import Annotated, Optional

from fastapi import APIRouter, status, UploadFile, Depends, Query, Path, HTTPException

from common.dependencies import get_current_user, get_current_optional_user, get_post_service
from schemas.common_response import CommonResponse
from schemas.pagination import PaginatedResponse, PaginationMeta
from schemas.post import PostsResponse, PostsResponseDetail, PostsUpdateRequest, PostsCreateRequest
from services.post_service import PostService
from models.base import User as UserTable  # 타입 힌트용

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=CommonResponse[PaginatedResponse[PostsResponse]], status_code=status.HTTP_200_OK)
async def get_posts(
        post_service: Annotated[PostService, Depends(get_post_service)],
        page: Annotated[int, Query(ge=1)] = 1,
        size: Annotated[int, Query(ge=1, le=100)] = 10,
        current_user: Annotated[Optional[UserTable], Depends(get_current_optional_user)] = None
):
    extracted_user_id = current_user.id if current_user else None

    posts, total = await post_service.get_post(page=page, limit=size, current_user_id=extracted_user_id)

    meta = PaginationMeta(page=page, limit=size, total_items=total)
    paginated_data = PaginatedResponse(content=posts, pagination=meta)

    return CommonResponse(
        status="success",
        message="게시물 목록 조회에 성공하였습니다.",
        data=paginated_data
    )


@router.get("/{post_id}", response_model=CommonResponse[PostsResponseDetail], status_code=status.HTTP_200_OK)
async def get_posts_detail(
        post_service: Annotated[PostService, Depends(get_post_service)],
        post_id: int = Path(..., description="조회할 게시글의 ID"),
        current_user: Annotated[Optional[UserTable], Depends(get_current_optional_user)] = None
):
    extracted_user_id = current_user.id if current_user else None

    posts_detail_data = await post_service.get_post_detail(post_id=post_id, current_user_id=extracted_user_id)

    return CommonResponse(
        status="success",
        message="게시물 상세 조회에 성공하였습니다.",
        data=posts_detail_data
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(
        post_service: Annotated[PostService, Depends(get_post_service)],
        current_user: Annotated[UserTable, Depends(get_current_user)],
        post_id: int = Path(..., description="삭제할 게시글의 ID"),
):
    await post_service.delete_post(post_id, current_user.id)
    return None


@router.put("/{post_id}", response_model=CommonResponse[PostsResponse], status_code=status.HTTP_200_OK)
async def update_posts(
        post_service: Annotated[PostService, Depends(get_post_service)],
        current_user: Annotated[UserTable, Depends(get_current_user)],
        update_request: PostsUpdateRequest,
        post_id: int = Path(..., description="수정할 게시물의 ID"),
):
    update_data = await post_service.update_post(post_id, update_request, current_user.id)

    return CommonResponse(
        status="success",
        message="성공적으로 게시물을 업데이트 하였습니다.",
        data=update_data
    )


@router.post("/", response_model=CommonResponse[PostsResponse], status_code=status.HTTP_201_CREATED, summary="게시물 생성")
async def create_posts(
        post_service: Annotated[PostService, Depends(get_post_service)],
        current_user: Annotated[UserTable, Depends(get_current_user)],
        user_create_post: PostsCreateRequest
):
    posts_data = await post_service.create_post(user_create_post, current_user.id)

    return CommonResponse(
        status="success",
        message="성공적으로 게시물을 작성하였습니다.",
        data=posts_data
    )
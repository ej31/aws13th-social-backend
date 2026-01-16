from typing import Annotated, Optional

from fastapi import APIRouter,status
from fastapi.params import Depends, Query, Path

from common.dependencies import get_current_user, get_current_optional_user
from schemas.common_response import CommonResponse
from schemas.pagination import PaginatedResponse
from schemas.post import PostsResponse, PostsResponseDetail, PostsUpdateRequest, PostsCreateRequest
from services.post_service import PostService

router = APIRouter(prefix="/posts",tags=["posts"])

@router.get("/",response_model=CommonResponse[PaginatedResponse[PostsResponse]],status_code=status.HTTP_200_OK)
async def get_posts(post_service: Annotated[PostService,Depends(PostService)],
                    page: Annotated[int,Query(ge=1)] = 1,# 페이지 번호 1 이상
                    size: Annotated[int,Query(ge=1,le=100)]=10):
        posts_data = await post_service.get_posts(page=page,limit=size)
        return CommonResponse(
            status = "success",
            message= "게시물 목록 조회에 성공하였습니다.",
            data = posts_data
        )

@router.get("/{post_id}",response_model=CommonResponse[PostsResponseDetail],status_code=status.HTTP_200_OK)
async def get_posts_detail(post_service: Annotated[PostService,Depends(PostService)],
                           post_id: int = Path(...,description="조회할 게시글의 ID"),
                           current_user_id: Annotated[dict | None, Depends(get_current_optional_user)] = None):
    #현재 current_user가 비인증 사용자가 아니라면 dict에서 id를 꺼냄
    user_id = current_user_id.get("id") if current_user_id else None

    posts_detail_data = await post_service.get_posts_detail(post_id=post_id,user_id=user_id)
    return CommonResponse(
        status = "success",
        message = "게시물 상세 조회에 성공하였습니다.",
        data = posts_detail_data
    )

@router.delete("/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(post_service:Annotated[PostService,Depends(PostService)],
                       current_user_id: Annotated[dict ,Depends(get_current_user)],
                       post_id: int = Path(...,description="삭제할 게시글의 ID"),):

    author_id= current_user_id.get("id")
    await post_service.delete_posts(post_id,author_id)
    return None

@router.put("/{post_id}",response_model= CommonResponse[PostsResponse],status_code=status.HTTP_200_OK)
async def update_posts(post_service: Annotated[PostService,Depends(PostService)],
                       current_user_id: Annotated[dict, Depends(get_current_user)],
                       update_request: PostsUpdateRequest,
                       post_id: int = Path(...,description="수정할 게시물의 ID"),
                       ):
    author_id= current_user_id.get("id")
    update_data = await post_service.update_posts(post_id,update_request,author_id)
    return CommonResponse(
        status = "success",
        message = "성공적으로 게시물을 업데이트 하였습니다.",
        data=update_data
    )

#summary는 간단하게 한줄 요약, description은 길게 설명해야 할 때
@router.post("/",response_model= CommonResponse[PostsResponse],status_code=status.HTTP_201_CREATED,summary="게시물 생성",description=(""))
async def create_posts(post_service: Annotated[PostService,Depends(PostService)],
                       current_user_id: Annotated[dict | None, Depends(get_current_user)],
                       user_create_post: PostsCreateRequest):

        author_id= current_user_id.get("id")
        posts_data = await post_service.create_post(user_create_post,author_id)
        return CommonResponse(
            status = "success",
            message = "성공적으로 게시물을 작성하였습니다.",
            data = posts_data
        )
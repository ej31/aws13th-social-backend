from typing import Annotated

from fastapi import APIRouter,status
from fastapi.params import Depends

from common.dependencies import get_current_user
from schemas.comment import CommentResponse, CommentCreateRequest, CommentUpdateRequest
from schemas.common_response import CommonResponse
from schemas.pagination import PaginatedResponse,PaginationMeta
from services.comment_service import CommentService

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])

@router.post("/",response_model=CommonResponse[CommentResponse],status_code=status.HTTP_200_OK)
async def create_comment(post_id:int,
                         req:CommentCreateRequest,
                         current_user:Annotated[dict,Depends(get_current_user)],
                         comment_service: Annotated[CommentService,Depends(CommentService)]):
    comment_data = await comment_service.create_comment(post_id,req,current_user["id"])
    return CommonResponse(
        status = "success",
        message = "성공적으로 댓글을 작성하였습니다.",
        data = comment_data
    )

@router.get("/",response_model=CommonResponse[PaginatedResponse[CommentResponse]],status_code=status.HTTP_200_OK)
async def get_comments(post_id:int,
                       comment_service: Annotated[CommentService,Depends(CommentService)],
                       page:int = 1,
                       limit:int = 10,):
    comment_data,total_count = await comment_service.get_all_comments(post_id,page,limit)
    paginated_data = PaginatedResponse(
        content = comment_data,
        pagination = PaginationMeta(
            page=page,
            limit=limit,
            total_items=total_count
        )
    )
    return CommonResponse(
        status = "success",
        message= "성공적으로 댓글 목록을 불러왔습니다.",
        data = paginated_data
    )


@router.patch("/{comment_id}", response_model=CommonResponse[CommentResponse],status_code=status.HTTP_200_OK)
async def update_comment(
        post_id: int,  # prefix에서 주입됨
        comment_id: int,  # 경로 매개변수에서 주입됨
        req: CommentUpdateRequest,
        current_user: Annotated[dict, Depends(get_current_user)],
        comment_service: Annotated[CommentService, Depends(CommentService)]
):
    # 서비스 레이어에서 작성자 권한 및 존재 여부 검증 수행
    updated_data = await comment_service.update_comment(comment_id, req, current_user["id"])

    return CommonResponse(
        status="success",
        message="댓글을 성공적으로 수정하였습니다.",
        data=updated_data
    )


@router.delete("/{comment_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
        post_id: int,
        comment_id: int,
        current_user: Annotated[dict, Depends(get_current_user)],
        comment_service: Annotated[CommentService, Depends(CommentService)]
):
    # 서비스 레이어에서 삭제 로직 수행
    await comment_service.delete_comment(comment_id, current_user["id"])

    return None
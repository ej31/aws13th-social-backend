from fastapi import APIRouter, Query
from schemas.comments import CommentCreate, CommentUpdate

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("")
async def get_comments(
        postId: int,
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1)
):
    """댓글 목록 조회"""
    # TODO: 댓글 목록 조회 로직 구현
    return {
        "status": "success",
        "data": [],
        "pagination": {}
    }

@router.get("/me")
async def get_my_comments(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1)
):
    """내가 쓴 댓글 목록"""
    # TODO: 실제 내 댓글 목록 조회 로직 구현
    return {
        "status": "success",
        "data": [],
        "pagination": {}
    }

@router.post("", status_code=201)
async def create_comment(comment: CommentCreate):
    """댓글 작성"""
    # TODO: 실제 댓글 작성 로직 구현
    return {
        "status": "success",
        "message": "댓글이 성공적으로 등록되었습니다.",
        "data": {}
    }

@router.patch("/{commentId}")
async def update_comment(commentId: int, comment: CommentUpdate):
    """댓글 수정"""
    # TODO: 실제 댓글 수정 로직 구현
    return {
        "status": "success",
        "message": "댓글이 수정되었습니다.",
        "data": {}
    }

@router.delete("/{commentId}", status_code=204)
async def delete_comment(commentId: int):
    """댓글 삭제"""
    # TODO: 실제 댓글 삭제 로직 구현
    return {
        "status": "success",
        "message": "댓글이 성공적으로 삭제되었습니다."
    }
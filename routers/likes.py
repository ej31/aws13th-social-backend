from fastapi import APIRouter, Query
from schemas.likes import LikeCreate

router = APIRouter(prefix="/likes", tags=["likes"])

@router.get("")
async def get_my_likes(
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1)
):
    """내가 좋아요한 게시글 목록 조회"""
    # TODO: 실제 좋아요 목록 조회 로직 구현
    return {
        "status": "success",
        "data": [],
        "pagination": {}
    }

@router.get("/status")
async def get_like_status(postId: int):
    """좋아요 상태 확인"""
    # TODO: 실제 좋아요 상태 확인 로직 구현
    return {
        "status": "success",
        "data": {
            "postId": postId,
            "totalLikes": 0,
            "isLiked": False
        }
    }

@router.post("", status_code=201)
async def create_like(like: LikeCreate):
    """좋아요 등록"""
    # TODO: 실제 좋아요 등록 로직 구현
    return {
        "status": "success",
        "message": "해당 게시글에 좋아요를 눌렀습니다.",
        "data": {}
    }

@router.delete("/posts/{postId}/likes/me", status_code=204)
async def delete_like(postId: int):
    """좋아요 삭제"""
    # TODO: 실제 좋아요 삭제 로직 구현
    return {
        "status": "success",
        "message": "좋아요가 취소되었습니다."
    }

from fastapi import APIRouter, FastAPI, HTTPException

router = APIRouter(prefix="/posts/{post_id}",tags=["likes"])

@router.post("/likes",summary="좋아요 등록",description= "로그인한 사용자가 특정 게시글에 좋아요를 등록하는 리소스.", tags=["likes"])
async def post_likes(post_id: int):
    return

@router.delete("/likes", summary="좋아요 삭제",description= "로그인한 사용자가 특정 게시글에 등록한 좋아요를 취소하는 리소스", tags=["likes"])
async def delete_likes(post_id: int):
    return

@router.get("/likes", summary="좋아요 상태 확인", description= "게시글의 좋아요 상태를 조회하는 리소스.", tags=["likes"])
async def get_likes(post_id: int):
    return
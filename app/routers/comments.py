from fastapi import APIRouter, FastAPI, HTTPException

router = APIRouter(prefix="/posts/{postId}",tags=["comments"])

@router.post("/comments", summary="댓글 작성", description= "게시글에 댓글을 작성합니다(로그인 필요)", tags=["comments"])
async def post_comments():
    return

@router.patch("/comments/{comment_id}", summary="댓글 수정", description= "본인이 작성한 댓글만 수정하는 리소스", tags=["comments"])
async def patch_comments():
    return

@router.delete("/comments/{comment_id}", summary="댓글 삭제", description= "본인이 작성한 댓글만 삭제하는 리소스", tags=["comments"])
async def delete_comments():
    return

@router.get("/comments", summary="댓글 목록 조회",description="특정 게시글의 댓글 목록을 조회하는 리소스.",tags=["comments"])
async def get_comments():
    return

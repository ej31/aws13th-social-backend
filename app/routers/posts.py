from fastapi import APIRouter, FastAPI, HTTPException

router = APIRouter(prefix="/posts",tags=["posts"])

@router.post("/", summary="게시글 작성", description="사용자가 게시글의 제목과 내용을 입력하고 게시글을 작성하는 리소스(로그인 필요)", tags=["posts"])
async def create_post():
    return

@router.patch("/{post_id}", summary="게시글 수정", description="본인이 작성한 글의 제목과 내용을 수정할 수 있습니다.(로그인 필요)", tags=["posts"])
async def patch_post():
    return

@router.delete("/{post_id}", summary="게시글 삭제",description="본인이 작성한 게시글을 삭제하는 리소스", tags=["posts"])
async def delete_post():
    return

@router.get("/", summary="게시글 목록 조회",description= "게시글 목록을 조회합니다(페이지네이션 적용)", tags=["posts"])
async def get_posts():
    return

@router.get("/", summary="게시글 검색",description= "keyword를 통해 게시글 검색하는 리소스", tags=["posts"])
async def get_posts_by_keywords():
    return

@router.get("/", summary="게시물 정렬",description= "게시물을 최신순, 조회수순, 좋아요순 등으로 정렬하는 리소스.", tags=["posts"])
async def get_sorted_keywords():
    return

@router.get("/{post_id}", summary="게시글 상세 조회",description= "게시글의 id값을 통해 게시글을 상세 조회하는 리소스.", tags=["posts"])
async def get_posts_by_id(post_id: int):
    return



from fastapi import APIRouter, Query
from schemas.posts import PostCreate, PostUpdate, PostDetail

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("")
async def get_posts(
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100),
        search: str | None = None,
        sort: str | None = None
):
    """게시물 목록 조회"""
    # TODO: 게시물 목록 조회 로직 구현
    return {
        "status": "success",
        "data": [],
        "query": {"search": search, "sort": sort},
        "pagination": {
            "page": page,
            "limit": limit,
            "totalCount": 0,
            "totalPages": 1
        }
    }

@router.get("/me")
async def get_my_posts(
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100),
):
    """내가 쓴 게시물 목록 조회"""
    # TODO: 내 게시물 목록 조회 로직 구현
    return {
        "status": "success",
        "data": [],
        "pagination": {}
    }

@router.get("/{postId}")
async def get_post(postId: int):
    """게시글 상세 조회"""
    # TODO: 게시글 상세 조회 로직 구현, 조회수 1 증가 로직 추가
    return {
        "status": "success",
        "data": {
            "postId": postId,
            "title": "게시글 상세 제목",
            "content": "게시글의 전체 본문 내용",
            "nickname": "작성자 닉네임",
            "profileImage": "https://example.com/profiles/img.png",
            "viewCount": 1,
            "likeCount": 0,
            "isLiked": False,
            "createdAt": "2026-01-16T00:00:00Z",
            "updatedAt": "2026-01-16T00:00:00Z"
        }
    }

@router.post("", status_code=201)
async def create_post(post: PostCreate):
    """게시글 작성"""
    # TODO: 게시글 작성 로직 구현
    return {
        "status": "success",
        "message": "게시글이 성공적으로 등록되었습니다.",
        "data": {}
    }

@router.patch("/{postId}")
async def update_post(postId: int, post: PostUpdate):
    """게시글 수정"""
    # TODO: 게시글 수정 로직 구현
    return {
        "status": "success",
        "message": "게시글이 성공적으로 수정되었습니다.",
        "data": {}
    }

@router.delete("/{postId}")
async def delete_post(postId: int):
    """게시글 삭제"""
    # TODO: 게시글 삭제 로직 구현
    return {
        "status": "success",
        "message": "게시글이 성공적으로 삭제되었습니다.",
    }
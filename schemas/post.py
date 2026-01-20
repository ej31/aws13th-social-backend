from schemas.common import Pagination
from pydantic import BaseModel,Field
from datetime import datetime


# 게시글 목록 조회
# GET/posts
# 1. 저자 정보
class AuthorInfo(BaseModel):
    author_email: str
    nickname: str
# 2. 게시글 요약정보
class PostPostSummary(BaseModel):
    post_id: str
    title: str
    author: AuthorInfo
    created_at: datetime
# 3. 페이지네이션 정보

# 4. 출력 정보
class PostListResponse(BaseModel):
    status: str = 'success'
    data: list[PostPostSummary]
    pagination: Pagination
# 게시글 검색
class PostSearchResponse(BaseModel):
    status: str = 'success'
    data: list[PostPostSummary]
    pagination: Pagination
# 게시글 정렬
class PostSortedResponse(BaseModel):
    status: str = 'success'
    data: list[PostPostSummary]
    pagination: Pagination
# 게시글 상세 조회
# 게시글 상세 내역
class PostDetail(BaseModel):
    post_id: str
    title: str
    content: str
    author: AuthorInfo
    created_at: datetime
class PostDetailResponse(BaseModel):
    status: str = 'success'
    data: PostDetail
# 댓글 목록 조회
class CommentItem(BaseModel):
    comment_id: str
    comment_content: str
    author: AuthorInfo
    created_at: datetime
    title: str
class CommentListResponse(BaseModel):
    status: str = 'success'
    data: list[CommentItem]
    pagination: Pagination
# 좋아요 상태 확인
class PostLikeStatus(BaseModel):
    post_id: str
    count_likes: int
    liked: bool
class PostLikeResponse(BaseModel):
    status: str = 'success'
    data: PostLikeStatus
# 게시글 작성
# Request 데이터 보낼 데이터
class PostCreateRequest(BaseModel):
    title: str
    content: str
# 응답 데이터
class CreationPost(BaseModel):
    post_id: str
    title: str = Field(...,min_length=1,description="게시글 제목")
    content: str = Field(...,min_length=1,description="게시글 내용")
    created_at: datetime
    author: AuthorInfo
class CreationPostResponse(BaseModel):
    status: str = 'success'
    data: CreationPost
# 게시글 수정
class PostUpdateRequest(BaseModel):
    title: str | None = None
    content: str | None = None
#수정 데이터
class PostUpdateData(BaseModel):
    post_id: str
    title: str
    content: str
    author: AuthorInfo
    updated_at: datetime
# 응답데이터
class PostUpdateResponse(BaseModel):
    status: str = 'success'
    data: PostUpdateData

# 댓글 작성
class CommentCreateRequest(BaseModel):
    content: str
class CommentCreateData(BaseModel):
    post_id: str
    comment_id: str
    author: AuthorInfo
    content: str
    created_at: datetime
class CommentCreateResponse(BaseModel):
    status: str = 'success'
    data: CommentCreateData

# 댓글 수정
class CommentUpdateRequest(BaseModel):
    content: str
class CommentUpdateData(BaseModel):
    post_id: str
    comment_id: str
    author: AuthorInfo
    content: str
    created_at: datetime
    updated_at: datetime
class CommentUpdateResponse(BaseModel):
    status: str = 'success'
    data: CommentUpdateData
# 좋아요 등록
class PostLikeCreateData(BaseModel):
    post_id: str
    author_email: str
    created_at: datetime
class PostLikeCreateResponse(BaseModel):
    status: str = 'success'
    data: PostLikeCreateData


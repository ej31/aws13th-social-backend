from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from schemas.pagenation import PaginationMeta


#게시물 스키마에 공통 모델
class PostsBase(BaseModel):
    title: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="게시물의 제목")
    content: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="게시물의 내용")

#게시글을 쓴 사용자에 대한 정보 (상속을 받지 않는 이유는 불 필요한 정보까지 같이 받게 됨)
class PostsAuthorResponse(BaseModel):
    id:str = Field(...,description="해시된 사용자 ID")
    nickname:str

#게시글 상세 조회
class PostsResponse(PostsBase):
    post_id: int = Field(...,description="게시물의 아이디")
    author: PostsAuthorResponse
    is_liked: bool = Field(...,description="현재 사용자가 게시물의 좋아요를 눌렀는가 확인")
    comment_count: int = Field(0,description="게시물의 댓글의 개수")
    likes: int = Field(0,description="게시물의 좋아요 개수")
    views: int = Field(0,description="게시물의 조회수 개수")
    created_at: datetime
    updated_at: datetime | None = None

#게시물 목록 조횐
class PostsListResponse(PostsBase):
    # content 안에는 PostResponse가 들어간다.
    content = List[PostsResponse]
    # 목록 하단에 페이지 번호를 표시하기 위해 사용한다.
    pagination: PaginationMeta

class PostsCreateRequest(PostsBase):
    pass

#게시물 업데이트 시 request
class PostsUpdateRequest(PostsBase):
    title: str | None = Field(None,min_length=1,max_length=100,description="글의 주인이 제목을 수정한다.")
    content: str | None = Field(None,min_length=1,max_length=255,description="글의 주인이 내용을 수정한다.")


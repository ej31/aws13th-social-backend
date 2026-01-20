from datetime import datetime, timezone

from pydantic import BaseModel, Field



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
    id: str = Field(...,description="해시된 사용자 ID")
    nickname:str

#게시물 목록을 조회할때는 PaginatedResponse(Generic[T], BaseModel) 함수를 이용함
class PostsResponse(PostsBase):
    post_id: int = Field(...,description="게시물의 아이디")
    author: PostsAuthorResponse
    is_liked: bool = Field(...,description="현재 사용자가 게시물의 좋아요를 눌렀는가 확인")
    comment_count: int = Field(0,description="게시물의 댓글의 개수")
    likes: int = Field(0,description="게시물의 좋아요 개수")
    views: int = Field(0,description="게시물의 조회수 개수")
    created_at: datetime
    updated_at: datetime | None = None

#JSON 내부에 저장할 때 사용하는 모델
class PostsCreateInternal(PostsBase):
    post_id: int
    author_id: int # 내부에서는 해시되지 않은 원본 ID를 저장한다.
    views: int = 0
    likes: int = 0
    comment_count: int = 0
    #default_factory는 새로운 객체가 만들어질 때 함수를 실행해서 새로운 값을 만들어냄
    #datetime.now().isoformat()으로 생성하게 되면 서버가 최초 실행된 날을 기준으로 날짜가 정해짐
    created_at: str = Field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
    updated_at: str | None = None

class PostsResponseDetail(PostsResponse):
    pass
    #comments: list[CommentResponse] 나중에 댓글 내용을 가져올 때 사용할 필드

class PostsCreateRequest(PostsBase):
    pass

#게시물 업데이트 시 request
class PostsUpdateRequest(PostsBase):
    title: str | None = Field(None,min_length=1,max_length=100,description="글의 주인이 제목을 수정한다.")
    content: str | None = Field(None,min_length=1,max_length=255,description="글의 주인이 내용을 수정한다.")

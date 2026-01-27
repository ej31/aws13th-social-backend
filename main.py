
from fastapi import FastAPI, Header, Path, Depends, Query, status, Response, HTTPException
from jose.constants import ALGORITHMS
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated, Literal, List
from datetime import datetime, timedelta
from jose import jwt
from utils.data import load_data, save_data
from passlib.context import CryptContext

app = FastAPI()

#회원가입
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    nickname: str = Field(min_length=4, max_length=8)
    profile_image: Optional[str] = None

class UserResponse(BaseModel):
    email: EmailStr
    nickname: str = Field(min_length=4, max_length=8)
    profile_image: Optional[str] = None
    created_at: datetime

@app.post("/users/", response_model=UserResponse)
async def signup(user_in: CreateUser):
    users = load_data("users.json")
    #이메일, 닉네임 중복 검사
    for u in users:
        if u["email"] == user_in.email:
            raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
        if u["nickname"] == user_in.nickname:
            raise HTTPException(status_code=400, detail="이미 존재하는 닉네임입니다.")

    hashed_password = pwd_context.hash(user_in.password)

    new_user = {
        "email": user_in.email,
        "password": hashed_password,
        "nickname": user_in.nickname,
        "profile_image": user_in.profile_image,
        "created_at": datetime.now()
    }

    users.append(new_user)
    save_data("users.json", users)

    return new_user

# 로그인
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int = 3600
    sign_in_at: datetime

class LoginResponse(BaseModel):
    status: str
    data: TokenData

fake_users_db = {
    "test@example.com": {
        "email": "test@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeKkl.9TaH1/drNsPw2",
        "id": 1
    }
}

def verify_password(plain_password, hashed_password): # 입력받은 비번과 DB비번 일치 확인
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict): # JWT 토큰 생성
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/auth/token", response_model=LoginResponse)
async def login_access_token(
        token_in: LoginRequest,
        authorization: Annotated[str | None, Header()] = None
):

    user = fake_users_db.get(token_in.email)

    if not user or not verify_password(token_in.password, user["hashed_password"]):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "이메일 또는 비밀번호가 없습니다."
        )

    access_token = create_access_token(data={"sub": user["email"]})
    refresh_token = create_access_token(data={"sub": user["email"], "type": "refresh"})

    return {
        "status": "success",
        "data": {
            "access_token": "temp_access_token",
            "refresh_token": "temp_refresh_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "sign_in_at": datetime.now()
        }
    }


# 프로필 조회
class ProfileResponseData(BaseModel):
    email: EmailStr
    nickname: str = Field(min_length=4, max_length=8)
    profile_image: Optional[str] = None
    created_at: datetime

class ProfileResponse(BaseModel):
    status: str
    data: ProfileResponseData

@app.get("/users/{nickname}", response_model=ProfileResponse)
async def get_profile(nickname: str):
    return {
        "status": "success",
        "data": {
            "email": "email",
            "nickname": nickname,
            "profile_image": "profile_image",
            "created_at": "created_at"
        }
    }


# 프로필 수정
class EditProfile(BaseModel):
    nickname: str = Field(min_length=4, max_length=8)
    profile_image: Optional[str] = None
    password: str = Field(min_length=8, max_length=16)

class EditProfileData(BaseModel):
    nickname: str = Field(min_length=4, max_length=8)
    profile_image: Optional[str] = None
    updated_at: datetime

class EditProfileResponse(BaseModel):
    status: str
    data: EditProfileData

@app.patch("/users/{nickname}", response_model=EditProfileResponse)
async def update_profile(nickname: str):
    return {
        "status": "success",
        "data": {
            "nickname": nickname,
            "profile_image": "profile_image",
            "updated_at": datetime.now()
        }
    }

# 회원 탈퇴
class DeleteProfileResponse(BaseModel):
    status: str
    message: str

@app.delete("/users/{nickname}", response_model=DeleteProfileResponse)
async def delete_profile(deleted_user: DeleteProfileResponse):
    return {
        "status": "success",
        "message": deleted_user.message
    }

# 특정 회원 조회
class SearchData(BaseModel):
    nickname: str = Field(min_length=4, max_length=8)
    profile_image: Optional[str] = None
    created_at: datetime

class SearchResponse(BaseModel):
    status: str
    data: SearchData

@app.get("/users/{nickname}", response_model=SearchResponse)
async def get_profile(
        nickname: Annotated[str, Path(min_length=4, max_length=8)],):
    return{
        "status": "success",
        "data": {
            "nickname": nickname,
            "profile_image": "profile_image",
            "created_at": datetime.now()
        }
    }


# 게시글 목록 조회
class SearchPostQuery(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    sort: Literal["created_at","updated_at"] = Field("created_at")

class PostItem(BaseModel):
    nickname: str = Field
    title: str
    created_at: datetime
    updated_at: datetime

class Pagination(BaseModel):
    page: int
    limit: int
    total: int

class PostListResponse(BaseModel):
    status: str
    data: List[PostItem]
    pagination: Pagination

@app.get("/posts", response_model=PostListResponse)
async def get_posts(
        params: SearchPostQuery = Depends()
):
    fetched_posts = []
    total_count = 0
    return{
        "status": "success",
        "data": fetched_posts,
        "pagination": {
            "page": params.page,
            "limit": params.limit,
            "total": total_count,
        }
    }


# 게시글 검색
class SearchDetailQuery(BaseModel):
    search: str = Field(min_length=1)
    search_type: Literal["title", "content"] = Field("title", description="검색 범위")

class PostDetailItem(BaseModel):
    nickname: str
    title: str
    post: str
    created_at: datetime

class PostDetailResponse(BaseModel):
    status: str
    data: PostDetailItem | None = None

@app.get("/posts/search", response_model=PostDetailResponse)
async def search_post(
    params: SearchDetailQuery = Depends()
):
    return{
        "status": "success",
        "data": None
    }


# 게시글 정렬
class Pagination(BaseModel):
    page: int
    limit: int
    total: int

class PostListItem(BaseModel):
    nickname: str
    title: str
    like_count: int
    created_post_at: datetime

class PostListResponse(BaseModel):
    status: str
    data: List[PostListItem]
    pagination: Pagination

@app.get("/posts", response_model=PostListResponse)
async def get_posts(
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100),
        sort: str = Query("created_at")
):
    return{
        "status": "success",
        "data": [
            {
                "nickname": "닉네임",
                "title": "게시글 제목",
                "like_count": "게시글 좋아요 수",
                "created_post_at": "datetime"
            }
        ],
        "pagination": {
            "page": 1,
            "limit": 20,
            "total": 100
        }
    }


# 게시글 상세 조회
class PostDetail(BaseModel):
    title: str
    post_id: int
    nickname: str
    post_content: str
    created_post_at: datetime
    post_updated_at: datetime

class PostDetailResponse(BaseModel):
    status: str
    data: PostDetailItem

@app.get("/posts/{post_id}")
async def get_post(

):
    return {
        "status": "success",
        "data": [
            {
                "post_id": 1234125,
                "nickname": "닉네임",
                "title": "게시글 제목",
                "post_content": "게시글 내용",
                "created_post_at": "datetime"
            }
        ]
    }


# 게시글 작성
class PostCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    post: str = Field(min_length=1, max_length=1000, alias="content")

class PostCreateData(BaseModel):
    post_id: int
    title: str
    post: str
    created_post_at: str

class PostCreateResponse(BaseModel):
    status: str
    data: PostCreateData

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostCreateResponse)
async def create_post(
    request: PostCreateRequest
):
    return {
        "status": "success",
        "data": {
            "post_id": 124567890,
            "title": request.title,
            "post": request.post,
            "created_post_at": "2026-01-04T12:00:00Z"
        }
    }


# 게시글 수정
class PostUpdateRequest(BaseModel):
    post_title: str = Field(..., min_length=1, max_length=100)
    post_content: str = Field(..., min_length=1, max_length=1000, alias="content")

class PostUpdateData(BaseModel):
    title: str
    content: str
    nickname: str

class PostUpdateResponse(BaseModel):
    status: str
    data: PostUpdateData
    post_created_at: datetime
    post_updated_at: datetime

@app.patch("/users/{nickname}/posts/{post_id}")
async def update_post(
        request: PostUpdateRequest
):
    return{
        "status": "success",
        "data": {
            "nickname": "닉네임",
            "title": "변경된 게시글 제목",
            "content": "변견된 게시글 내용",
            "post_created_at": "datetime",
            "post_updated_at": datetime.now()
        }
    }


# 게시글 삭제
class DeletePost(BaseModel):
    status: str
    message: str

@app.delete("/posts/{nickname}", response_model=DeletePost)
async def delete_post(deleted_post: DeletePost):
    return {
        "status": "success",
        "message": deleted_post.message
    }


# 내가 쓴 게시물 목록
class PostsWriteData(BaseModel):
    post_id: int
    nickname: str
    title: str
    created_post_at: datetime

class PostWriteResponse(BaseModel):
    status: str
    data: PostsWriteData

@app.get("users/me/posts")
async def get_my_post(
        post_id: int
):
    return {
        "status": "success",
        "data": [
            {
                "post_id": 1234125,
                "nickname": "닉네임",
                "title": "게시글 제목",
                "created_post_at": "datetime"
            }
        ]
    }


# 댓글 목록 조회
class CommentItem(BaseModel):
    post_id: int
    nickname: str
    comment: str
    like_count: int
    created_at: datetime
    updated_at: datetime

class Pagination(BaseModel):
    page: int
    limit: int = Field(ge=1, le=100)
    sort: Literal["created_at", "like_count"] = "created_at"

class CommentListResponse(BaseModel):
    status: str
    data: List[CommentItem]
    pagination: Pagination

@app.get("/posts/{post_id}/comments")
async def get_comments(
        post_id: int,
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100),
        sort: str = Query("created_at")
):
    return{
        "status": "success",
        "data": [
            {
                "post_id": 1234125,
                "nickname": "닉네임",
                "comment": "댓글 내용",
                "like_count": "댓글 공감 수",
                "created_at": "datetime"
            }
        ],
        "pagination": {
            "page": 1,
            "limit": 20,
            "sort": "created_at"
        }
    }


# 댓글 작성
class CommentCreateRequest(BaseModel):
    comment: str = Field(min_length=1, max_length=1000, alias="content")
    # TODO: authorization
    nickname: str

class CommentCreateData(BaseModel):
    nickname: str
    comment: str
    comment_id: int
    comment_created_at: datetime

class CommentCreateResponse(BaseModel):
    status: str
    data: CommentCreateData

@app.post("/posts/comments")
async def create_comment(
        request: CommentCreateRequest
):
    return{
        "status": "success",
        "data": {
            "nickname": "닉네임",
            "comment": "댓글 내용",
            "comment_id": 1234125,
            "comment_created_at": datetime.now()
        }
    }


# 댓글 수정
class CommentUpdateRequest(BaseModel):
    comment: str = Field(min_length=1, max_length=1000, alias="content")

class CommentUpdateData(BaseModel):
    comment_id: int
    nickname: str
    comment: str
    created_at: datetime
    updated_at: datetime

class CommentUpdateResponse(BaseModel):
    status: str
    data: CommentUpdateData

@app.patch("/posts/{post_id}/comments/{comment_id}")
async def update_comment(
        request: CommentUpdateRequest
):
    return{
        "status": "success",
        "data": {
            "comment_id": 1234125,
            "nickname": "닉네임",
            "comment": "댓글 수정 내용",
            "created_at": "datetime",
            "updated_at": datetime.now()
        }
    }


# 댓글 삭제
@app.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 내가 쓴 댓글 목록
class MyCommentsItem(BaseModel):
    comment_id: int
    comment: str
    like_count: int
    created_at: datetime

class Pagination(BaseModel):
    page: int
    limit: int
    sort: Literal["created_at", "like_count"] = "created_at"

class MyCommentsResponse(BaseModel):
    status: str
    data: List[MyCommentsItem]
    pagination: Pagination

@app.get("/users/{nickname}/comments", response_model=MyCommentsResponse)
async def get_my_comments(
        nickname: str,
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100)
):
    return{
        "status": "success",
        "data": [
            {
                "comment_id": 1234125,
                "comment": "댓글 내용",
                "like_count": 123,
                "created_at": datetime.now()
            }
        ],
        "pagination": {
            "page": 1,
            "limit": 20,
            "sort": "created_at"
        }
    }


# 좋아요 등록
# TODO: Authorization
class LikeRequest(BaseModel):
    like: bool

class LikeRegistrationData(BaseModel):
    title: str
    like_count: int
    created_at: datetime

class LikeRegistrationResponse(BaseModel):
    status: str
    data: LikeRegistrationData

@app.post("/posts/{post_id}/likes", response_model=LikeRegistrationResponse)
async def like_registration(
        post_id: int,
        request: LikeRequest
):
    return{
        "status": "success",
        "data": {
            "title": "닉네임",
            "like_count": 10,
            "created_at": datetime.now()
        }
    }


# 좋아요 취소
class LikeCancelRequest(BaseModel):
    like: bool

class LikeCancelData(BaseModel):
    title: str
    like_count: int
    created_at: datetime

class LikeCancelResponse(BaseModel):
    status: str
    data: LikeCancelData

@app.delete("/posts/{post_id}/likes", response_model=LikeCancelResponse)
async def like_cancel(
        post_id: int,
        request: LikeCancelRequest
):
    return {
        "status": "success",
        "data": {
            "title": "게시글 제목",
            "like_count": 9,
            "created_at": datetime.now()
        }
    }


# 좋아요 상태 확인
class LikeStatusPagination(BaseModel):
    page: int
    limit: int
    sort: Literal["created_at", "like_total"] = "created_at"

class LikeStatusItem(BaseModel):
    title: str
    like_count: int
    like_total: int
    created_at: datetime

class LikeStatusResponse(BaseModel):
    status: str
    data: List[LikeStatusItem]
    pagination: LikeStatusPagination

@app.get("/users/{nickname}/posts/likes", response_model=LikeStatusResponse)
async def get_likes(
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100),
        sort: str = Query("created_at")
):
    return{
        "status": "success",
        "data": [
            {
                "title": "게시물 제목",
                "like_count": 10,
                "like_total": 333,
                "created_at": datetime.now()
            }
        ],
        "pagination": {
            "page": 1,
            "limit": 20,
            "sort": "created_at"
        }
    }


# 내가 좋아요한 게시글 목록
class ILikedListPagination(BaseModel):
    page: int
    limit: int
    sort: Literal["liked_at", "created"] = "liked_at"
    total: int

class ILikedListItem(BaseModel):
    title: str
    like_count: int
    created_at: datetime

class ILikedListResponse(BaseModel):
    status: str
    data: List[ILikedListItem]
    pagination: ILikedListPagination

@app.get("/users/me/likes", response_model=ILikedListResponse)
async def i_liked(
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100),
        sort: str = Query("liked_at")
):
    return{
        "status": "success",
        "data": [
            {
                "title": "게시글 제목",
                "like_count": 10,
                "created_at": datetime.now()
            }
        ],
        "pagination": {
            "page": 1,
            "limit": 20,
            "total": 100
        }
    }
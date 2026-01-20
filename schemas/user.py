# users의 관련된 pydantic 스키마 작성하는 부분
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re


# 회원가입 Post/users 부분
# 이제 클라이언트가 회원가입할때
class CreateUser(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="8자 이상, 영문/숫자/특수 문자 포함")
    nickname: str
    profile_image: str | None = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:    # v는 입력값(비밀번호)
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('비밀번호에 영문자가 포함되어야 합니다')
        if not re.search(r'\d', v):
            raise ValueError('비밀번호에 숫자가 포함되어야 합니다')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>₩]', v):
            raise ValueError('비밀번호에 특수문자가 포함되어야 합니다')
        return v


# 회원가입하고 나서
class ResponseUser(BaseModel):
    status: str = "success"

    class Userinfo(BaseModel):
        email: EmailStr
        nickname: str
        profile_image: str | None
        created_at: datetime

    data: Userinfo


# 프로필 수정 put/user/me
# 프로필 입력 할때
class UpdateUserRequest(BaseModel):
    current_password: str
    nickname: str
    profile_image: str | None = None
    new_password: str | None = None

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return CreateUser.validate_password(v)

# 수정된 프로필 응답
class UpdateUserResponse(BaseModel):
    status: str = "success"

    class Userinfo(BaseModel):
        email: EmailStr
        nickname: str
        profile_image: str | None
        updated_at: datetime

    data: Userinfo


# 회원 로그인 요청할때
class LoginUserRequest(BaseModel):
    email: EmailStr = Field(..., description="가입한 이메일 주소")
    password: str = Field(..., min_length=8, description="비밀번호")


class TokenData(BaseModel):
    token_type: str = "Bearer"  # "token" 대신 "token_type" 권장
    access_token: str
    expires_in: int


# 회원 로그인 응답
class LoginUserResponse(BaseModel):
    status: str = "success"
    data: TokenData


# 내 프로필 조회
# 요청할께 없다
class GetProfile(BaseModel):
    status: str = "success"

    class Userinfo(BaseModel):
        email: EmailStr
        nickname: str
        profile_image: str | None
        created_at: datetime

    data: Userinfo


# 특정 회원 조회
class OtherUserProfileResponse(BaseModel):
    status: str = "success"

    class Userinfo(BaseModel):
        email: EmailStr
        nickname: str
        profile_image: str | None
        created_at: datetime

    data: Userinfo


# 내가쓴 게시글 목록
class UserPostSummary(BaseModel):
    post_id: str
    title: str
    created_at: datetime


class Pagination(BaseModel):
    page: int
    limit: int
    total: int


class MyPostsResponse(BaseModel):
    status: str = "success"
    data: list[UserPostSummary]
    pagination: Pagination


# 내가 작성한 댓글
class PostInComment(BaseModel):
    post_id: str
    title: str


class CommentSummary(BaseModel):
    comment_id: str
    post: PostInComment
    content: str
    created_at: datetime
    updated_at: datetime


class MyCommentsResponse(BaseModel):
    status: str = "success"
    data: list[CommentSummary]
    pagination: Pagination


# 내가 좋아요한 게시글 목록
class AuthorInfo(BaseModel):
    author_email: str
    nickname: str


class LikesPostSummary(BaseModel):
    post_id: str
    title: str
    author: AuthorInfo
    count_likes: int
    count_comment: int
    created_at: datetime


class MyLikesResponse(BaseModel):
    status: str = "success"
    data: list[LikesPostSummary]
    pagination: Pagination

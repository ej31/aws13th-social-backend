from typing import Annotated
from datetime import datetime
from fastapi import FastAPI, Query, Body, status, Header, Response
from enum import Enum
from pydantic import EmailStr
from schemas import user
from schemas.user import CreateUser, UpdateUserRequest, LoginUserRequest, GetProfile, OtherUserProfileResponse


class PostSortType(str, Enum):
    '''
    최신순,조회수순,좋아요순
    '''
    latest = "latest"
    views = "views"
    likes = "likes"


app = FastAPI()


############### 먼저 Users 엔드포인트 작성 ############
# 내 프로필 조회
@app.get("/users/me", response_model=user.GetProfile)
async def read_users_me(
        authorization: Annotated[str, Header(description="로그인 시 발급받은 토큰을 전달")],
):
    # 지금은 DB가 없으니 그냥 예시 데이터를 리턴!
    return {
        "status": "success",
        "data": {
            "email": "example@naver.com",  # 여기에 누가 오든 일단 이걸 보여줌
            "nickname": "abc",
            "profile_image": "image.123",
            "created_at": "2026-01-04T12:00:00Z"
        }
    }


# 특정 회원 조회
@app.get("/users/{email}", response_model=OtherUserProfileResponse)
async def get_user(
        email: EmailStr
):
    return {
        "status": "success",
        "data": {
            "email": email,
            "nickname": "abc",
            "profile_image": "image.123",
            "created_at": "2026-01-04T12:00:00Z"
        }
    }


# 내가 쓴 게시글 목록
@app.get("/users/me/posts", response_model=user.MyPostsResponse)
async def get_user_posts(
        authorization: Annotated[str, Header(description="Bearer access token")],
        page: int = Query(default=1, ge=1, description="페이지 번호"),
        limit: int = Query(default=20, ge=1, le=100, description="페이지당 항목 수")
):
    return {
        "status": "success",
        "data": [
            {
                "post_id": "1",
                "title": "첫 글",
                "created_at": "2026-01-16T12:00:00Z"
            },
            {
                "post_id": "2",
                "title": "두 번째",
                "created_at": "2026-01-16T12:00:00Z"
            }
        ],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": 100
        }
    }


# 내가 작성한 댓글
@app.get("/users/me/comments", response_model=user.MyCommentsResponse)
async def get_user_comments(
        authorization: Annotated[str, Header(description="Bearer access token")],
        page: int = Query(default=1, ge=1, description="페이지 번호"),
        limit: int = Query(default=20, ge=1, le=100, description="페이지당 항목 수"),
):
    return {
        "status": "success",
        "data": [
            {
                "id": "comment_1",
                "post": {
                    "id": "1",
                    "title": "게시글 제목"
                },
                "content": "내가 작성한 댓글",
                "created_at": "2026-01-04T12:00:00Z",
                "updated_at": "2026-01-05T12:00:00Z"
            }
        ],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": 100
        }
    }


# 내가 좋아요한 게시글 목록
@app.get("/users/me/likes", response_model=user.MyLikesResponse)
async def get_user_likes(
        authorization: Annotated[str, Header(description="로그인 토큰으로 인증")],
        page: int = Query(default=1, ge=1, description="페이지 번호"),
        limit: int = Query(default=20, ge=1, le=100, description="페이지당 항목 수")
):
    return {
        "status": "success",
        "data": [
            {
                "post_id": "1",
                "title": "내가 좋아요를 누른 게시글 제목",
                "author": {
                    "author_id": "admin",
                    "nickname": "abc"
                },
                "count_likes": 12,
                "count_comment": 90,
                "created_at": "2026-01-04T12:00:00Z"
            }
        ],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": 100
        }
    }


# 회원 가입
@app.post("/users", response_model=user.ResponseUser, status_code=201)
async def post_users(
        user_data: Annotated[CreateUser, Body()]
):
    current_time = datetime.datetime.now().isoformat()
    return {"status": "success",
            "data": {
                "email": user_data.email,
                "nickname": user_data.nickname,
                "profile_image": user_data.profile_image,
                "created_at": current_time
            }
            }


# 프로필 수정
@app.put("/users/me", response_model=user.UpdateUserResponse)
async def put_user(
        update_data: Annotated[UpdateUserRequest, Body()],
        authorization: Annotated[str, Header(description="로그인 시 발급받은 토큰")]
):
    update_time = datetime.datetime.now().isoformat()
    # 실제 구현시 토큰에서 사용자 이메일을 추출해야 함
    return {"status": "success",
            "data": {
                "email": update_data.email,
                "nickname": update_data.nickname,
                "profile_image": update_data.profile_image,
                "updated_at": update_time
            }
            }


# 회원 탈퇴
@app.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        authorization: Annotated[str, Header(description="로그인 시 발급되는 토큰")]
):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


######Posts############
# GET 먼저 생성
# 게시글 목록 조회
@app.get("/posts")
async def get_posts(
        page: int = Query(default=1, ge=1, description="페이지 번호"),
        limit: int = Query(default=20, ge=1, le=100, description="페이지당 항목 수")
):
    return {"page": page, "limit": limit}


# 게시글 검색
@app.get("/posts/search")
async def get_posts_by_keyword(
        keyword: str = Query(min_length=1),
        page: int = Query(default=1, ge=1, description="페이지 번호"),
        limit: int = Query(default=20, ge=1, le=100, description="페이지당 항목 수")
):
    return {"keyword": keyword, "page": page, "limit": limit}


# 게시글 정렬
@app.get("/posts/sorted")
async def get_posts_sorted(
        sort: PostSortType,
        page: int = Query(default=1, ge=1, description="페이지 번호"),
        limit: int = Query(default=20, ge=1, le=100, description="페이지당 항목 수")
):
    return {"sort": sort, "page": page, "limit": limit}


# 게시글 상세조회
@app.get("/posts/{post_id}")
async def get_post(
        post_id: str
):
    return {"post_id": post_id}


# 댓글 목록 조회
@app.get("/posts/{post_id}/comments")
async def get_post_comments(
        post_id: str,
        page: int = Query(default=1, ge=1, description="페이지 번호"),
        limit: int = Query(default=20, ge=1, le=100, description="페이지당 항목 수")
):
    return {"post_id": post_id, "page": page, "limit": limit}


# 좋아요 상태 확인
@app.get("/posts/{post_id}/likes")
async def get_post_likes(
        post_id: str
):
    return {"post_id": post_id}


# 게시글 작성
@app.post("/posts")
async def post_post():
    pass


# 게시글 수정
@app.put("/posts/{post_id}")
async def put_post(
        post_id: str
):
    return {"post_id": post_id}


# 게시글 삭제
@app.delete("/posts/{post_id}")
async def delete_post(
        post_id: str
):
    return {"post_id": post_id}


# 댓글 작성 (특정 게시글에 댓글을 작성합니다.)
@app.post("/posts/{post_id}/comments")
async def post_comment(
        post_id: str
):
    return {"post_id": post_id}


# 댓글 수정
@app.put("/posts/{post_id}/comments/{comment_id}")
async def change_comment(
        post_id: str,
        comment_id: str
):
    return {"post_id": post_id, "comment_id": comment_id}


# 좋아요 등록
@app.post("/posts/{post_id}/likes")
async def post_like(
        post_id: str
):
    return {"post_id": post_id}


# 좋아요 취소
@app.delete("/posts/{post_id}/likes")
async def delete_like(
        post_id: str
):
    return {"post_id": post_id}


############Comments##################
# 댓글 삭제
@app.delete("/comments/{comment_id}")
async def delete_comment(
        comment_id: str
):
    return {"comment_id": comment_id}


######### auth ############
# 회원 로그인
@app.post("/auth/token", response_model=user.LoginUserResponse, status_code=status.HTTP_201_CREATED)
async def auth_token(
        login_data: Annotated[LoginUserRequest, Body()]
):
    return {"status": "success",
            "data": {
                "token_type": "Bearer",
                "access_token": "token_1234",
                "expires_in": 3600
            }
            }

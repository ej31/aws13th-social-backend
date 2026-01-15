from fastapi import APIRouter, FastAPI, HTTPException
from app.routers.auth import hash_password
from app.schemas.users import UserLoginRequest, UserSignupRequest
from app.utils.data import read_users, write_users
from datetime import datetime

router = APIRouter(prefix="/users",tags=["users"])

@router.post("/", summary="유저 회원가입",description="회원가입: 이메일, 비밀번호, 닉네임, 프로필 이미지(선택)로 가입", tags=["users"])
async def post_user(new_user: UserSignupRequest):
    users = read_users()

    new_user = {
        "id": len(users) + 1,
        "email": new_user.email,
        "nickname": new_user.nickname,
        "password_hash": hash_password(new_user.password),
        "profile_image": new_user.profile_image,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    users.append(new_user)
    write_users(users)

    # 해싱된 비밀번호도 담기면 안되서 따로 respon_user를 만듬
    response_user = {
        "id": new_user["id"],
        "email": new_user["email"],
        "nickname": new_user["nickname"],
        "profile_image": new_user["profile_image"],
        "created_at": new_user["created_at"]
    }
    return {"status": "success", "data": response_user}

@router.post("/login", summary="유저 로그인", description="로그인: 이메일/비밀번호로 인증 후 토큰 발급", tags=["users"])
async def login_user(request: UserLoginRequest):
    return

@router.patch("/me", summary="프로필 수정", description="닉네임, 프로필 이미지, 비밀번호 변경", tags=["users"])
async def patch_user(request: UserLoginRequest):
    return

@router.delete("/me", summary="회원 삭제", description="계정을 삭제합니다.", tags=["users"])
async def delete_user(request: UserLoginRequest):
    return

@router.get("/me", summary="내 프로필 조회", description="로그인한 사용자 본인 정보를 조회합니다", tags=["users"])
async def get_me(request: UserLoginRequest):
    return

@router.get("/{user_id}", summary="특정 회원 조회", description="다른 사용자의 공개 프로필 조회", tags=["users"])
async def get_user_by_id(request: UserLoginRequest, user_id: int):
    return

@router.get("/me/posts",summary="내가 쓴 게시글 목록", description="로그인한 사용자가 쓴 게시글을 조회하여 목록을 보여주는 리소스.", tags=["users"])
async def get_user_by_id(request: UserLoginRequest, user_id: int):
    return

@router.get("/me/comments", summary="내가 쓴 댓글 목록 조회", description="로그인 한 사용자의 댓글만 조회하여 목록을 보여주는 리소스.", tags=["users"])
async def get_user_comments():
    return

@router.get("/me/likes/liked_posts", summary="내가 좋아요한 게시글 목록 조회", description="로그인한 사용자가 좋아요를 등록한 게시글 목록을 조회하기 위한 리소스.", tags=["users"])
async def get_user_liked_posts():
    return
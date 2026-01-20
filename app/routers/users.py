from fastapi import APIRouter, HTTPException, Depends, status
from app.routers.auth import hash_password, verify_password
from app.schemas.users import UserLoginRequest, UserSignupRequest, UserProfileUpdateRequest, MyProfile
from app.utils.data import read_users, write_users
from datetime import datetime, timezone
from app.dependencies.auth import get_current_user
from app.routers.auth import verify_password, hash_password
from typing import Annotated

import uuid

router = APIRouter(prefix="/users",tags=["users"])

@router.post("/", summary="유저 회원가입",description="회원가입: 이메일, 비밀번호, 닉네임, 프로필 이미지(선택)로 가입", tags=["users"])
async def post_user(new_user: UserSignupRequest):
    users = read_users()

    new_user = {
        "id": str(uuid.uuid4()),
        "email": new_user.email,
        "nickname": new_user.nickname,
        "hash_password": hash_password(new_user.password),
        "profile_image": new_user.profile_image,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
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

@router.patch("/me", summary="프로필 수정", description="닉네임, 프로필 이미지, 비밀번호 변경", tags=["users"])
async def patch_user(change_profile: UserProfileUpdateRequest, current_user: Annotated[dict, Depends(get_current_user)],):
    users = read_users()

    idx = None
    for i, u in enumerate(users):
        if u.get("id") == current_user.get("id"):
            idx = i
            break

    if idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )

    user = users[idx]

    if change_profile.nickname is not None:
        users[idx]["nickname"] = change_profile.nickname

    if change_profile.profile_image is not None:
        users[idx]["profile_image"] = change_profile.profile_image

    if change_profile.password is not None:
        if change_profile.current_password is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "비밀번호를 변경하기 위해서는 현재 비밀번호를 입력해야합니다."
            )

        saved_hash = user.get("hash_password")
        if not saved_hash or not verify_password(change_profile.current_password, saved_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "현재 비밀번호가 올바르지 않습니다."
            )

        user["hash_password"] = hash_password(change_profile.password)


    write_users(users)

    response = {
        "status" : "success",
        "nickname" : user["nickname"],
        "profile_image" : user["profile_image"],
        "created_at" : user["created_at"]
    }
    return response



@router.delete("/me", summary="회원 삭제", description="계정을 삭제합니다.", tags=["users"])
async def delete_user(current_user: Annotated[dict, Depends(get_current_user)],):
    users = read_users()

    idx = None
    for i, u in enumerate(users):
        if u.get("id") == current_user.get("id"):
            idx = i
            break
    if idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    if users[idx].get("is_deleted"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이미 탈퇴한 사용자입니다."
        )


    users[idx]["is_deleted"] = True
    write_users(users)

    return {"status" : "success", "message" : "회원 탈퇴가 완료되었습니다."}

@router.get("/me", summary="내 프로필 조회", description="로그인한 사용자 본인 정보를 조회합니다", tags=["users"])
async def get_me(current_user: Annotated[dict, Depends(get_current_user)],):
    users = read_users()
    for u in users:
        if u.get("id") == current_user.get("id"):
            return {
                "status" : "success",
                "data" :{
                    "id" : u.get("id"),
                    "nickname" : u.get("nickname"),
                    "profile_image" : u.get("profile_image"),
                    "created_at" : u.get("created_at")
                }
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="회원을 찾을 수 없습니다."
    )



@router.get("/{user_id}", summary="특정 회원 조회", description="다른 사용자의 공개 프로필 조회", tags=["users"])
async def get_user_by_id(user_id: str):
    users = read_users()
    for u in users:
        if u.get("id") == user_id:
            return {
                "status" : "success",
                "data" : {
                    "id": u.get("id"),
                    "nickname": u.get("nickname"),
                    "profile_image": u.get("profile_image"),
                    "created_at": u.get("created_at")
                }
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="조회하려는 사용자 정보를 찾을 수 없습니다."
    )


@router.get("/me/posts",summary="내가 쓴 게시글 목록", description="로그인한 사용자가 쓴 게시글을 조회하여 목록을 보여주는 리소스.", tags=["users"])
async def get_my_posts(request: UserLoginRequest, user_id: int):
    return

@router.get("/me/comments", summary="내가 쓴 댓글 목록 조회", description="로그인 한 사용자의 댓글만 조회하여 목록을 보여주는 리소스.", tags=["users"])
async def get_user_comments():
    return

@router.get("/me/likes/liked_posts", summary="내가 좋아요한 게시글 목록 조회", description="로그인한 사용자가 좋아요를 등록한 게시글 목록을 조회하기 위한 리소스.", tags=["users"])
async def get_user_liked_posts():
    return
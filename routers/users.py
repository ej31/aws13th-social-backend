
from fastapi import APIRouter, Depends, HTTPException

from schemas.user import UserOut, NickNameUpdateIn, PasswordChangeIn
from utils.auth import get_current_user, verify_password, hash_password
from utils.data import read_json, write_json

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# 내 프로필 조회 (DONE!)
@router.get("/me",response_model=UserOut)
def get_profile(current_user : dict = Depends(get_current_user)):
    users = read_json("users.json", default=[])
    user = next((u for u in users if u["id"] == current_user["id"]), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(f"내 프로필 조회 : {user['nickname']}의 프로필 ")
    return user

# 특정 회원 조회 (DONE!)
@router.get("/{user_id}",response_model=UserOut)
def get_user(user_id: int):
    users = read_json("users.json", default=[])
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(f"특정 회원 프로필 조회 : {user['nickname']} 프로필 ")
    # return 이후에 HTTP 응답에서 Response_model에 정의한 필드만 나가고
    # print(user)에서는 모든 값이 출력됨
    return user

# 프로필 닉네임 수정 (DONE!)
@router.patch("/me",response_model=UserOut)
def update_profile_nickname(
        payload: NickNameUpdateIn,
        current_user : dict = Depends(get_current_user)):

    users = read_json("users.json", default=[])

    user = next((u for u in users if u["id"] == current_user["id"]), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if any(u["nickname"] == payload.nickname and u["id"] != current_user["id"] for u in users):
        raise HTTPException(status_code=409, detail="Nickname already taken")

    user["nickname"] = payload.nickname
    write_json("users.json", users)
    return user

# 프로필 이미지 수정
@router.put("/me/profile-image")
def update_profile_image():
    pass

# 비밀번호 변경 (DONE!)
@router.patch("/me/password")
def change_password(
        payload: PasswordChangeIn,
        current_user : dict = Depends(get_current_user),
):
    users = read_json("users.json", default=[])

    user = next((u for u in users if u["id"] == current_user["id"]), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(payload.old_password, current_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    user["hashed_password"] = hash_password(payload.new_password)
    write_json("users.json", users)

# 회원 탈퇴
@router.delete("me")
def delete_profile():
    pass

# 내가 쓴 게시글 목록
@router.get("/me/posts")
def get_user_posts():
    pass

# 내가 쓴 댓글 목록
@router.get("/me/comments")
def get_user_comments():
    pass

# 내가 좋아요한 게시글 목록
@router.get("/me/likes")
def get_user_likes():
    pass

# 좋아요 상태 확인
@router.get("/me/posts/likes/summary")
def get_total_likes():
    pass


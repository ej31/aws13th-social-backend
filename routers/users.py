
from fastapi import APIRouter, Depends

from schemas.comment import CommentOut
from schemas.post import PostOut
from schemas.user import UserOut, NickNameUpdateIn
from utils.auth import get_current_user
from utils.data import read_json, write_json

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# 내 프로필 조회
@router.get("/me",response_model=UserOut)
def getprofile(payload: UserOut):
    pass

# 특정 회원 조회
@router.get("/{user_id}",response_model=UserOut)
def getuser(payload: UserOut):
    pass

# 프로필 닉네임 수정 (작성중)
@router.patch("/me",response_model=UserOut)
def update_profile_nickname(
        payload: NickNameUpdateIn,
        current_user = Depends(get_current_user)):

    users = read_json("users.json", default=[])

    user = next(u for u in users if u["id"] == current_user["id"])
    user["nickname"] = payload.nickname

    write_json("users.json", users)
    return user

# 프로필 이미지 수정
@router.put("/me/profile-image",response_model=UserOut)
def update_profile_image(payload: UserOut):
    pass

# 비밀번호 변경
@router.put("/me/password",response_model=UserOut)
def update_profile_password(payload: UserOut):
    pass

# 회원 탈퇴
@router.delete("me",response_model=UserOut)
def delete_profile(payload: UserOut):
    pass

# 내가 쓴 게시글 목록
@router.get("/me/posts",response_model=PostOut)
def get_user_posts(payload: UserOut):
    pass

# 내가 쓴 댓글 목록
@router.get("/me/comments",response_model=CommentOut)
def get_user_comments(payload: UserOut):
    pass

# 내가 좋아요한 게시글 목록
@router.get("/me/likes",response_model=CommentOut)
def get_user_likes(payload: UserOut):
    pass

# 좋아요 상태 확인
@router.get("/me/posts/likes/summary",response_model=PostOut)
def get_total_likes(payload: UserOut):
    pass


from fastapi import APIRouter, status, Body, HTTPException
from typing import Annotated
from datetime import datetime, timezone
from schemas import user
from utils.data import load_data, save_data
from utils.auth import hash_password

router = APIRouter(prefix="/users", tags=["users"])


# 회원가입
@router.post("", response_model=user.ResponseUser, status_code=status.HTTP_201_CREATED)
async def post_users(
        user_data: Annotated[user.CreateUser, Body()]
):
    users = load_data("users.json")

    hashed_password = hash_password(user_data.password)

    # 중복 가입 방지 로직
    existing_emails = {u['email'] for u in users}

    if user_data.email in existing_emails:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "error": {
                    "code": "BAD_REQUEST",
                    "message": "이미 가입된 이메일입니다."
                }
            }
        )
    current_time = datetime.now(timezone.utc).isoformat()

    # 파일에 저장할 데이터 객체를 만듭니다.
    new_user_entry = {
        "email": user_data.email,
        "password": hashed_password,  # 평문 대신 해시값 저장!
        "nickname": user_data.nickname,
        "profile_image": user_data.profile_image,
        "created_at": current_time
    }

    # 리스트에 추가하고 파일로 씁니다.
    try:
        users.append(new_user_entry)
        save_data(users, "users.json")
    except Exception as e:
        # 파일 저장 실패 시 500 에러를 반환하여 클라이언트에게 알림
        print(f"파일 저장 중 에러 발생: {e}")  # 서버 로그용
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "서버 내부 오류로 인해 데이터를 저장하지 못했습니다."
                }
            }
        )
    return {
        "status": "success",
        "data": {
            "email": new_user_entry["email"],
            "nickname": new_user_entry["nickname"],
            "profile_image": new_user_entry["profile_image"],
            "created_at": new_user_entry["created_at"]
        }
    }

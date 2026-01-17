from fastapi import APIRouter, status, HTTPException
from schemas.user import UserCreate, UserRegistrationResponse
from utils.data import load_json, save_json, generate_id
from datetime import datetime

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "",
    response_model=UserRegistrationResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(user: UserCreate):
    # 1. 기존 유저 데이터 로드
    users = load_json("users.json")

    # 2. 중복 이메일 검사 (비즈니스 로직)
    if any(u["email"] == user.email for u in users):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 이메일입니다."
        )

    # 3. 새로운 유저 객체 생성
    new_user = {
        "id": generate_id("user", users),
        "email": user.email,
        "nickname": user.nickname,
        "profile_image_url": user.profile_image_url,
        "password": user.password,  # 2단계에서 해싱 처리 예정
        "created_at": datetime.now().isoformat()
    }

    # 4. 리스트에 추가 및 파일 저장
    users.append(new_user)
    save_json("users.json", users)

    return {
        "status": "success",
        "data": new_user
    }
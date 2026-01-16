from fastapi import APIRouter, HTTPException, status
from schemas.user import UserLogin
from utils.auth import verify_password, create_access_token
from utils.data import load_data, ensure_user_fields

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/tokens")
def login(data: UserLogin):

    users = load_data("users")
    matched_user = None

    #이메일이 같은 계정만 찾기
    for user in users:
        ensure_user_fields(user)  # is_deleted 기본값 보정

        if (
            user.get("email", "").lower() == data.email.lower()
            and user.get("is_deleted") is False
        ):
            matched_user = user
            break

    # 비밀번호 맞으면 토큰 발급, 탈퇴 후 재가입도
    if matched_user and verify_password(data.password, matched_user["password"]):
        access_token = create_access_token(
            data={"sub": matched_user["userId"]}
        )
        return {
            "status": "success",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": 3600,
            }
        }


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "status": "error",
            "data": {"message": "이메일 또는 비밀번호가 일치하지 않습니다."}
        }
    )

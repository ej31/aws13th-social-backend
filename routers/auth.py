from fastapi import APIRouter, HTTPException, Response, Request
from schemas.users import UserLogin, LoginResponse
from utils.data import load_json, find_by_field, add_item, find_by_id
from utils.auth import verify_password, create_access_token, create_refresh_token, verify_token
from datetime import datetime, timezone


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/tokens")
async def login(user: UserLogin, response: Response):
    """로그인"""
    users = load_json("users.json")

    # 이메일로 사용자 찾기
    db_user = find_by_field(users, "email", user.email)
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "code": "UNAUTHORIZED",
                "message": "이메일 또는 비밀번호가 잘못되었습니다."
            }
        )

    # 비밀번호 검증
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "code": "UNAUTHORIZED",
                "message": "이메일 또는 비밀번호가 잘못되었습니다."
            }
        )

    # AccessToken 생성
    access_token = create_access_token(
        data={"userId": db_user["userId"], "email": db_user["email"]}
    )

    # RefreshToken 생성 및 저장
    refresh_token_data = create_refresh_token(db_user["userId"])
    add_item("refresh_tokens.json", refresh_token_data, id_field="tokenId")

    # RefreshToken을 HttpOnly 쿠키로 설정
    response.set_cookie(
        key="refreshToken",
        value=refresh_token_data["token"],
        httponly=True,  # JavaScript에서 접근 불가 (XSS 방지)
        secure=False,  # 개발환경에서는 False, 프로덕션에서는 True (HTTPS)
        samesite="lax",  # CSRF 방지
        max_age=7 * 24 * 60 * 60  # 7일
    )

    return {
        "status": "success",
        "message": "로그인에 성공하였습니다.",
        "data": {
            "userId": db_user["userId"],
            "nickname": db_user["nickname"],
            "accessToken": access_token,
            "tokenType": "Bearer",
            "expiresIn": 60 * 60
        }
    }

@router.post("/tokens/refresh")
async def refresh_access_token(request: Request, response: Response):
    """RefreshToken으로 새로운 AccessToken 발급"""
    # 쿠키에서 refreshToken 읽기
    refresh_token = request.cookies.get("refreshToken")

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "code": "UNAUTHORIZED",
                "message": "리프레시 토큰이 없습니다."
            }
        )

    refresh_tokens = load_json("refresh_tokens.json")
    users = load_json("users.json")

    # RefreshToken 찾기
    token_data = find_by_field(refresh_tokens, "token", refresh_token)
    if not token_data:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "code": "UNAUTHORIZED",
                "message": "유효하지 않은 리프레시 토큰입니다."
            }
        )

    # 만료 확인
    if datetime.fromisoformat(token_data["expiresAt"]) < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "code": "UNAUTHORIZED",
                "message": "만료된 리프레시 토큰입니다."
            }
        )

    # 사용자 정보 조회
    user = find_by_id(users, token_data["userId"], id_field="userId")
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 새로운 AccessToken 발급
    new_access_token = create_access_token(
        data={"userId": user["userId"], "email": user["email"]}
    )

    return {
        "status": "success",
        "data": {
            "accessToken": new_access_token,
            "tokenType": "Bearer",
            "expiresIn": 60 * 60
        }
    }



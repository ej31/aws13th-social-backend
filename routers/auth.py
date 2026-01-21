from fastapi import APIRouter, HTTPException, Response, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import os
from schemas.users import UserLogin, LoginResponse
from database import get_db
from repositories import UserRepository, RefreshTokenRepository
from utils.auth import verify_password, create_access_token, create_refresh_token, hash_refresh_token
from datetime import datetime, timezone


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/tokens")
async def login(user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    """로그인"""
    user_repo = UserRepository(db)
    token_repo = RefreshTokenRepository(db)

    # 이메일로 사용자 찾기
    db_user = await user_repo.get_by_email(user.email)
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
    if not verify_password(user.password, db_user.password):
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
        data={"userId": db_user.userId, "email": db_user.email}
    )

    # RefreshToken 생성 및 저장
    refresh_token_data = create_refresh_token(db_user.userId)

    # 평문 토큰은 쿠키로 전송, 해시만 DB에 저장
    await token_repo.create(
        token_hash=refresh_token_data["tokenHash"],
        user_id=refresh_token_data["userId"],
        expires_at=refresh_token_data["expiresAt"]
    )

    await db.commit()

    # RefreshToken을 HttpOnly 쿠키로 설정
    response.set_cookie(
        key="refreshToken",
        value=refresh_token_data["token"],
        httponly=True,  # JavaScript에서 접근 불가 (XSS 방지)
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",  # 개발환경에서는 False, 프로덕션에서는 True (HTTPS)
        samesite="lax",  # CSRF 방지
        max_age=7 * 24 * 60 * 60,  # 7일
        path="/auth/tokens/refresh"
    )

    return {
        "status": "success",
        "message": "로그인에 성공하였습니다.",
        "data": {
            "userId": db_user.userId,
            "nickname": db_user.nickname,
            "accessToken": access_token,
            "tokenType": "Bearer",
            "expiresIn": 60 * 60
        }
    }


@router.post("/tokens/refresh")
async def refresh_access_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """RefreshToken으로 새로운 AccessToken 발급"""
    user_repo = UserRepository(db)
    token_repo = RefreshTokenRepository(db)

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

    # RefreshToken 찾기
    refresh_token_hash = hash_refresh_token(refresh_token)
    token_data = await token_repo.get_by_hash(refresh_token_hash)
    if not token_data:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "code": "UNAUTHORIZED",
                "message": "유효하지 않은 리프레시 토큰입니다."
            }
        )

    # 만료 확인 (timezone-aware datetime으로 변환)
    now = datetime.now(timezone.utc)
    expires_at = token_data.expiresAt
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "code": "UNAUTHORIZED",
                "message": "만료된 리프레시 토큰입니다."
            }
        )

    # 사용자 정보 조회
    user = await user_repo.get_by_id(token_data.userId)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "code": "NOT_FOUND",
                "message": "사용자를 찾을 수 없습니다."
            }
        )

    # RefreshToken Rotation
    # 1. 기존 RefreshToken 삭제(일회성)
    await token_repo.delete(token_data.tokenId)

    # 2. 새로운 RefreshToken 생성 및 저장
    new_refresh_token_data = create_refresh_token(user.userId)
    await token_repo.create(
        token_hash=new_refresh_token_data["tokenHash"],
        user_id=new_refresh_token_data["userId"],
        expires_at=new_refresh_token_data["expiresAt"]
    )

    await db.commit()

    # 3. 새 RefreshToken을 HttpOnly 쿠키로 설정
    response.set_cookie(
        key="refreshToken",
        value=new_refresh_token_data["token"],
        httponly=True,
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/auth/tokens/refresh"
    )

    # 4. 새로운 AccessToken 발급
    new_access_token = create_access_token(
        data={"userId": user.userId, "email": user.email}
    )
    return {
        "status": "success",
        "data": {
            "accessToken": new_access_token,
            "tokenType": "Bearer",
            "expiresIn": 60 * 60
        }
    }

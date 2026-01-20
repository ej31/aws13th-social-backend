from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate, UserResponse, UserUpdate, UserDelete, UserPublicResponse
from database import get_db
from repositories import UserRepository, RefreshTokenRepository
from utils.auth import hash_password, verify_password, get_current_user
from models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=201)
async def create_user(request: UserCreate, db: AsyncSession = Depends(get_db)):
    """회원가입"""
    user_repo = UserRepository(db)

    # 이메일 중복 체크
    if await user_repo.email_exists(request.email):
        raise HTTPException(
            status_code=409,
            detail={
                "status": "error",
                "code": "DUPLICATE_RESOURCE",
                "message": "이미 사용 중인 정보(이메일/닉네임)입니다."
            }
        )

    # 비밀번호 해싱
    hashed_password = hash_password(request.password)

    # 사용자 저장
    new_user = await user_repo.create(
        email=request.email,
        password=hashed_password,
        nickname=request.nickname,
        profile_image=request.profileImage
    )

    return {
        "status": "success",
        "message": "회원가입이 완료되었습니다.",
        "data": {
            "userId": new_user.userId,
            "email": new_user.email,
            "nickname": new_user.nickname,
            "createdAt": new_user.createdAt
        }
    }


@router.get("/me")
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """내 프로필 조회"""
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(current_user["userId"])

    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "code": "NOT_FOUND",
                "message": "사용자를 찾을 수 없습니다."
            }
        )

    return {
        "status": "success",
        "data": {
            "userId": user.userId,
            "email": user.email,
            "nickname": user.nickname,
            "profileImage": user.profileImage,
            "createdAt": user.createdAt
        }
    }


@router.patch("/me")
async def update_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """프로필 수정"""
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(current_user["userId"])

    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "code": "NOT_FOUND",
                "message": "사용자를 찾을 수 없습니다."
            }
        )

    # 비밀번호 변경 시 currentPassword 확인
    update_data = {}
    if user_update.password:
        if not user_update.currentPassword:
            raise HTTPException(status_code=400, detail="현재 비밀번호를 입력해주세요.")

        if not verify_password(user_update.currentPassword, user.password):
            raise HTTPException(status_code=403, detail="현재 비밀번호가 일치하지 않습니다.")

        update_data["password"] = hash_password(user_update.password)

    if user_update.nickname:
        update_data["nickname"] = user_update.nickname
    if "profileImage" in user_update.model_fields_set:
        update_data["profileImage"] = user_update.profileImage

    # 업데이트
    updated_user = await user_repo.update(current_user["userId"], **update_data)

    return {
        "status": "success",
        "message": "프로필 정보가 성공적으로 수정되었습니다.",
        "data": {
            "userId": updated_user.userId,
            "nickname": updated_user.nickname,
            "profileImage": updated_user.profileImage,
            "updatedAt": updated_user.updatedAt
        }
    }


@router.delete("/me")
async def delete_user(
    user_delete: UserDelete,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """회원탈퇴"""
    user_repo = UserRepository(db)
    token_repo = RefreshTokenRepository(db)

    user = await user_repo.get_by_id(current_user["userId"])

    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "code": "NOT_FOUND",
                "message": "사용자를 찾을 수 없습니다."
            }
        )

    # 비밀번호 확인
    if not verify_password(user_delete.password, user.password):
        raise HTTPException(
            status_code=403,
            detail={
                "status": "error",
                "code": "FORBIDDEN",
                "message": "비밀번호가 일치하지 않습니다."
            }
        )

    # 해당 사용자의 모든 refreshToken 삭제
    await token_repo.delete_by_user_id(current_user["userId"])

    # 사용자 삭제 (CASCADE로 인해 관련 데이터도 자동 삭제)
    await user_repo.delete(current_user["userId"])

    return {
        "status": "success",
        "message": "회원 탈퇴가 성공적으로 처리되었습니다."
    }

@router.get("/{userId}")
async def get_user(userId: int, db: AsyncSession = Depends(get_db)):
    """특정 회원 조회"""
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(userId)

    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "code": "NOT_FOUND",
                "message": "요청하신 리소스를 찾을 수 없습니다."
            }
        )

    return {
        "status": "success",
        "data": {
            "userId": user.userId,
            "nickname": user.nickname,
            "profileImage": user.profileImage,
            "createdAt": user.createdAt
        }
    }

"""
회원 API
- 회원가입
- 내 프로필 조회
- 프로필 수정
- 회원 탈퇴
- 특정 회원 조회
"""
from fastapi import APIRouter, HTTPException, status

from app.schemas.user import (
    UserSignupRequest,
    UserUpdateRequest,
    UserProfileResponse,
    UserPublicResponse
)
from app.schemas.common import APIResponse
from app.api.deps import UserRepo, CurrentUser

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=APIResponse[UserProfileResponse])
def signup(
    user_data: UserSignupRequest,
    user_repo: UserRepo
):
    """
    회원가입
    """
    # 이메일 중복 체크
    if user_repo.exists_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 등록된 이메일입니다"
        )
    
    # 닉네임 중복 체크
    if user_repo.exists_by_nickname(user_data.nickname):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 닉네임입니다"
        )
    
    # 사용자 생성
    user = user_repo.create_user(
        email=user_data.email,
        password=user_data.password,
        nickname=user_data.nickname,
        profile_image=user_data.profile_image
    )
    
    # 비밀번호 제거 후 반환
    user_response = {k: v for k, v in user.items() if k != "password"}
    
    return APIResponse(
        status="success",
        data=UserProfileResponse(**user_response)
    )


@router.get("/me", response_model=APIResponse[UserProfileResponse])
def get_my_profile(current_user: CurrentUser):
    """
    내 프로필 조회
    """
    # 비밀번호 제거
    user_response = {k: v for k, v in current_user.items() if k != "password"}
    
    return APIResponse(
        status="success",
        data=UserProfileResponse(**user_response)
    )


@router.patch("/me", response_model=APIResponse[UserProfileResponse])
def update_my_profile(
    updates: UserUpdateRequest,
    current_user: CurrentUser,
    user_repo: UserRepo
):
    """
    프로필 수정
    """
    user_id = current_user["user_id"]
    
    # 수정할 데이터 추출 (None이 아닌 값만)
    update_data = updates.model_dump(exclude_none=True)
    
    # 수정할 내용이 없으면 에러
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="수정할 내용이 없습니다"
        )
    
    # 닉네임 중복 체크 (변경하려는 경우만)
    if "nickname" in update_data:
        existing_user = user_repo.find_by_nickname(update_data["nickname"])
        if existing_user and existing_user["user_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용 중인 닉네임입니다"
            )
    
    # 사용자 정보 수정
    success = user_repo.update_user(user_id, **update_data)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="프로필 수정에 실패했습니다"
        )
    
    # 수정된 사용자 정보 조회
    updated_user = user_repo.find_by_user_id(user_id)
    user_response = {k: v for k, v in updated_user.items() if k != "password"}
    
    return APIResponse(
        status="success",
        data=UserProfileResponse(**user_response)
    )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    current_user: CurrentUser,
    user_repo: UserRepo
):
    """
    회원 탈퇴
    """
    user_id = current_user["user_id"]
    
    success = user_repo.delete_user(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="회원 탈퇴에 실패했습니다"
        )
    
    # 204 No Content는 응답 본문이 없음
    return None


@router.get("/{user_id}", response_model=APIResponse[UserPublicResponse])
def get_user_profile(
    user_id: int,
    user_repo: UserRepo
):
    """
    특정 회원 조회
    """
    user = user_repo.find_by_user_id(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    # 공개 정보만 반환
    user_response = UserPublicResponse(
        user_id=user["user_id"],
        nickname=user["nickname"],
        profile_image=user["profile_image"],
        created_at=user["created_at"]
    )
    
    return APIResponse(
        status="success",
        data=user_response
    )
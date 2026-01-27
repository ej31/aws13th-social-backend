from typing import Annotated

from fastapi import APIRouter, status, UploadFile, HTTPException
from fastapi.params import Form, File, Depends
from pydantic import EmailStr

from schemas.common_response import CommonResponse
from common.dependencies import get_user_service, get_current_user  # get_user_service로 명칭 변경 권장
from common.security import decode_id
from schemas.user import (
    SignupRequest, UserResponse, UserLoginRequest,
    TokenData, UserUpdateRequest, UserSearchResponse
)
from services.user_service import UserService
from models.base import User as UserTable  # 타입 힌트용

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=CommonResponse[UserResponse], status_code=status.HTTP_200_OK)
async def get_my_user_info(
        current_user: Annotated[UserTable, Depends(get_current_user)],
):
    return CommonResponse(
        status="success",
        message="내 프로필 조회 성공",
        data=current_user
    )


@router.post("/", response_model=CommonResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def signup(
        user_service: Annotated[UserService, Depends(get_user_service)],
        email: Annotated[EmailStr, Form(...)],
        password: Annotated[str, Form(...)],
        nickname: Annotated[str, Form(...)],
        profile_image: Annotated[UploadFile | None, File()] = None
):
    signup_data = SignupRequest(email=email, password=password, nickname=nickname,profile_image=profile_image)
    new_user = await user_service.signup_user(signup_data, profile_image)

    return CommonResponse(
        status="success",
        message="회원가입에 성공했습니다.",
        data=new_user
    )


@router.post("/auth/tokens", response_model=CommonResponse[TokenData], status_code=status.HTTP_200_OK)
async def login(
        login_data: UserLoginRequest,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    result = await user_service.login_user(login_data)
    return CommonResponse(
        status="success",
        message="로그인에 성공하였습니다.",
        data=result
    )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
        user_service: Annotated[UserService, Depends(get_user_service)],
        current_user: Annotated[UserTable, Depends(get_current_user)]
):
    await user_service.delete_user(current_user.email)
    return None


@router.patch("/me", response_model=CommonResponse[UserResponse], status_code=status.HTTP_200_OK)
async def update_me(
        user_service: Annotated[UserService, Depends(get_user_service)],
        current_user: Annotated[UserTable, Depends(get_current_user)],
        current_password: Annotated[str, Form(...)],
        password: Annotated[str | None, Form()] = None,
        nickname: Annotated[str, Form()] = None,
        profile_image: Annotated[UploadFile | None, File()] = None
):
    user_update_data = UserUpdateRequest(
        nickname=nickname,
        password=password,
        current_password=current_password
    )
    result = await user_service.update_user(current_user.email, user_update_data, profile_image)

    return CommonResponse(
        status="success",
        message="회원 정보 업데이트에 성공하였습니다.",
        data=result
    )


@router.get("/{user_id}", response_model=CommonResponse[UserSearchResponse], status_code=status.HTTP_200_OK)
async def get_user_by_id(
        user_id: str,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    decoded_id = decode_id(user_id)
    if decoded_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="유효하지 않은 사용자입니다.")

    result = await user_service.find_user_by_id(decoded_id)

    return CommonResponse(
        status="success",
        message="회원 정보를 찾았습니다.",
        data=result
    )
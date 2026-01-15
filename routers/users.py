from typing import Annotated

from fastapi import APIRouter, status, UploadFile
from fastapi.params import Form, File, Depends
from pydantic import EmailStr
from fastapi import HTTPException
from common.common import CommonResponse
from common.dependencies import get_auth_service, get_current_user
from common.security import encode_id, decode_id
from schemas.user import SignupRequest, UserResponse, UserLoginRequest, TokenData, UserQueryResponse, UserUpdateRequest, \
    UserUpdateResponse
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
@router.get("/me",response_model=CommonResponse[UserResponse],status_code=status.HTTP_200_OK)
async def get_my_user_info(
        current_user: Annotated[dict, Depends(get_current_user)],
):
    user_data = current_user.copy()
    user_data["id"] = encode_id(user_data["id"])

    return CommonResponse(
        status="success",
        message="내 프로필 조회 성공",
        data=user_data
    )

@router.post(path="/", response_model=CommonResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def signup(
        user_service: Annotated[UserService, Depends(get_auth_service)],
        email: EmailStr = Form(...),  # ...은 requirement(필수), EmailStr (@ 형식으로 들어온 데이터)
        password: str = Form(...),
        nickname: str = Form(...),
        profile_image: UploadFile = File(None),
):
    signup_data = SignupRequest(email=email, password=password, nickname=nickname)
    new_user = await user_service.signup_user(signup_data, profile_image)

    return CommonResponse(
        status="success",
        message="회원가입에 성공했습니다.",
        data=new_user
    )

@router.post("/auth/tokens", response_model=CommonResponse[TokenData], status_code=status.HTTP_200_OK)
async def login(login_data: UserLoginRequest, user_service: Annotated[UserService, Depends(get_auth_service)]):
    result = await user_service.login_user(login_data)
    return CommonResponse(
        status="success",
        message="로그인에 성공하였습니다.",
        data=result
    )

@router.delete("/me",status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(user_service: Annotated[UserService, Depends(get_auth_service)],
                    current_user: Annotated[dict, Depends(get_current_user)]):
    await user_service.delete_user(current_user["email"])
    return None

@router.patch("/me",response_model=CommonResponse[UserUpdateResponse],status_code=status.HTTP_200_OK)
async def update_me(user_service: Annotated[UserService, Depends(get_auth_service)],
                    current_user: Annotated[dict, Depends(get_current_user)],
                    current_password: str = Form(...),
                    password: str | None = Form(None),
                    nickname: str = Form(None),
                    profile_image: UploadFile = File(None)
                    ):
    user_update_data = UserUpdateRequest(nickname=nickname, password=password,current_password=current_password)
    result = await user_service.update_user(current_user["email"],user_update_data,profile_image)
    return CommonResponse(
        status="success",
        message="회원 정보 업데이트에 성공하였습니다.",
        data=result
    )

@router.get("/{user_id}",response_model= CommonResponse[UserQueryResponse],status_code=status.HTTP_200_OK)
async def get_user_by_id(
                         user_id: str,
                         user_service: Annotated[UserService,Depends(get_auth_service)]):

    decoded_id = decode_id(user_id)
    if decoded_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="유효하지 않은 사용자입니다.")
    result = await user_service.find_user_by_id(decoded_id)

    return CommonResponse(
        status="success",
        message="회원 정보를 찾았습니다.",
        data=result
    )
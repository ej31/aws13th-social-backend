from typing import Annotated
from fastapi import APIRouter, status, UploadFile
from fastapi.params import Form, File, Depends
from pydantic import EmailStr

from common.dependencies import get_auth_service
from schemas.user import SignupRequest, UserResponse
from common.common import CommonResponse
from services.user_service import UserService
router= APIRouter(prefix="/users",tags=["users"])
@router.post(path= "/",response_model= CommonResponse[UserResponse],status_code=status.HTTP_201_CREATED)
async def signup(
    user_service: Annotated[UserService, Depends(get_auth_service)],
    email: EmailStr = Form(...), #...은 requirement(필수), EmailStr (@ 형식으로 들어온 데이터)
    password: str = Form(...),
    nickname: str = Form(...),
    profileImage: UploadFile = File(None),
):
    signup_data = SignupRequest(email=email,password=password,nickname=nickname)
    new_user = await user_service.signup_user(signup_data,profileImage)

    return CommonResponse(
        messages="회원가입에 성공했습니다.",
        data=new_user
    )
#
# @router.post("/login",response_model= CommonResponse[TokenData],status_code=status.HTTP_200_OK)
# async def login(login_data: UserLogin):
#     return True

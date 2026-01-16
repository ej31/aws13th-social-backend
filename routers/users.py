from fastapi import APIRouter, Depends, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from models.auth import UserSignUp, UserLogin, UserUpdate
from models.user import AuthResponse, UserPublic
from services.auth_service import signup_user, login_user
from services.user_service import get_my_profile,get_user_profile,update_my_profile,delete_my_account
from dependencies.auth import get_current_user
from datetime import datetime, timezone

"""
Users리소스 유의사항
- 개발 편의상 비밀번호 생성의 검증규칙(대문자, 특수문자 등등)은 자릿수값(최소2자, 최대50자)만 체크하도록 간소화한다.
- 개발 편의상 요청으로 들어온 비밀번호는 평문화 한다.(원래는 요청값 전송 즉시 해쉬화 하고, 평문 비밀번호는 삭제)
- DB저장 로직을 제외함으로, 해쉬된 비밀번호 및 users의 필드는 저장되지 않는다.
- JWT토큰은 임의로 생성된 secret값을 가진다. 
- UUID사용 하여 users구분값인 무작위 user_id생성 이후 user_id로 토큰 생성
"""

router = APIRouter(tags=["users"])

@router.post("/auth/signup",response_model=AuthResponse,status_code=status.HTTP_201_CREATED)
async def signup(form_data: Annotated[UserSignUp, Depends(UserSignUp.as_form)]):
    user, token, expires = signup_user(form_data)
    return AuthResponse(
        access_token=token,
        expires_in=expires,
        user=UserPublic(**user),
        issued_at=datetime.now(timezone.utc),
    )

@router.post("/auth/login",response_model=AuthResponse)
async def login(data: Annotated[UserLogin, Depends(OAuth2PasswordRequestForm)],
    form_data: OAuth2PasswordRequestForm = Depends()):
    # data = UserLogin
    user, token, expires = login_user(data)
    return AuthResponse(
        access_token=token,
        expires_in=expires,
        user=UserPublic(**user),
        issued_at=datetime.now(timezone.utc),
    )

@router.get("/users/me",response_model=UserPublic)
async def get_user_me(current_user: Annotated[dict, Depends(get_current_user)]):
    return get_my_profile(current_user)

@router.get("/users/{user_id}", response_model=UserPublic)
async def get_user(user_id: str):
    return get_user_profile(user_id)

@router.patch("/users/me",response_model=UserPublic)
async def update_user(
        update_data : Annotated[UserUpdate, Depends(UserUpdate.as_form)],
        current_user:  Annotated[dict, Depends(get_current_user)]
):
    patch_dict = update_data.model_dump(exclude_unset=True, mode="json")
    return update_my_profile(current_user, patch_dict)


@router.delete("/users/me",status_code=status.HTTP_200_OK)
async def delete_user(
        current_user: Annotated[dict, Depends(get_current_user)]
):
    delete_my_account(current_user)
    return {"user_id": "삭제되었음"}

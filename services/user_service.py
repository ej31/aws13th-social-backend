import os
from typing import Annotated

from util.file_upload import FileUtil
from fastapi import HTTPException, status, Depends, UploadFile

from common.config import settings
from common.security import hash_password, encode_id, verify_password
from common.jwt import create_access_token, create_refresh_token

from repositories.user_repository import UserRepository
from models.base import User as UserTable
from schemas.user import SignupRequest, UserLoginRequest, UserUpdateRequest


class UserService:
    def __init__(self, user_repo: Annotated[UserRepository, Depends(UserRepository)]) -> None:
        self.user_repo = user_repo

    async def signup_user(self, signup_data: SignupRequest, profile_image: UploadFile | None):
        if await self.user_repo.find_by_email(str(signup_data.email)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="해당 이메일은 이미 가입되었습니다.",
            )

        image_url = FileUtil.as_url(os.path.join(settings.upload_dir, "default.png"))
        if profile_image:
            image_url = await FileUtil.validate_and_save_image(profile_image)

        new_user = UserTable(
            email=signup_data.email,
            nickname=signup_data.nickname,
            password=hash_password(signup_data.password),
            profile_image=image_url
        )

        saved_user = await self.user_repo.add(new_user)

        return {
            "id": encode_id(saved_user.id),
            "email": saved_user.email,
            "nickname": saved_user.nickname,
            "profile_image": saved_user.profile_image,
            "created_at": saved_user.created_at
        }

    async def login_user(self, login_data: UserLoginRequest):
        user = await self.user_repo.find_by_email(str(login_data.email))

        if not user or not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다."
            )

        access_token = create_access_token(subject=user.email)
        refresh_token = create_refresh_token(subject=user.email)

        # 리프레시 토큰 업데이트 (필요 시 필드 추가 필요)
        # user.refresh_token = refresh_token
        # await self.user_repo.update(user)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
        }

    async def delete_user(self, email: str):
        user = await self.user_repo.find_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="유저를 찾을 수 없습니다."
            )

        if user.profile_image:
            FileUtil.delete_file(user.profile_image)

        await self.user_repo.delete_by_email(email)

    async def update_user(self, email: str, update_data: UserUpdateRequest, profile_image: UploadFile | None):
        user = await self.user_repo.find_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다."
            )

        if not verify_password(update_data.current_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="현재 비밀번호가 일치하지 않습니다."
            )

        update_dict = update_data.model_dump(exclude={"current_password", "password"}, exclude_unset=True)
        for key, value in update_dict.items():
            setattr(user, key, value)

        if update_data.password:
            if verify_password(update_data.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="새 비밀번호는 이전과 달라야 합니다."
                )
            user.password = hash_password(update_data.password)

        if profile_image:
            if user.profile_image:
                FileUtil.delete_file(user.profile_image.filename)
            user.profile_image = await FileUtil.validate_and_save_image(profile_image)

        await self.user_repo.update(user)
        return user

    async def find_user_by_id(self, user_id: int):
        target_user = await self.user_repo.find_by_id(user_id)
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="해당 유저를 찾을 수 없습니다."
            )
        return target_user
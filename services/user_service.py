import os
from datetime import datetime, timezone
from typing import Annotated

from util.file_upload import FileUtil
from fastapi import HTTPException, status, Depends
from fastapi import UploadFile

from common.config import settings
from common.security import hash_password, encode_id, verify_password
from common.jwt import create_access_token, create_refresh_token
from repositories.user_repository import UserRepository
from schemas.user import SignupRequest, UserLoginRequest, UserUpdateRequest, UserCreateInternal


class UserService:
    # service에서 jwt 의존성을 주입 받지 않는 이유는 이미 router에서 jwt로 인증을 받았기 때문이다.
    def __init__(self, user_repo: Annotated[UserRepository, Depends(UserRepository)]) -> None:
        self.user_repo = user_repo

    async def signup_user(self, signup_data: SignupRequest, profile_image: UploadFile | None):
        if self.user_repo.find_by_email(str(signup_data.email)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="해당 이메일은 이미 가입되었습니다.",
            )
        #기본 이미지 경로 공통 처리
        default_path = os.path.join(settings.upload_dir,"default.png")
        image_url = FileUtil.as_url(default_path)

        if profile_image:
            #업로드 시에도 as_url 메서드가 호출 되어서 저장 경로 통일
            image_url = await FileUtil.validate_and_save_image(profile_image)

        user_id = self.user_repo.get_next_id()

        new_user = UserCreateInternal(
            email = signup_data.email,
            nickname = signup_data.nickname,
            password = hash_password(signup_data.password),
            id= user_id,
            profile_image = image_url,
            created_at = datetime.now(timezone.utc).isoformat(),
        )


        saved_user = self.user_repo.save(new_user.model_dump())

        response_data = saved_user.copy()
        response_data["id"] = encode_id(saved_user["id"])

        return response_data

    async def login_user(self, login_data: UserLoginRequest):
        user = self.user_repo.find_by_email(str(login_data.email))

        # 유저가 없거나 비밀번호가 틀렸을 경우
        if not user or not verify_password(login_data.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다."
            )

        access_token = create_access_token(subject=user["email"])
        refresh_token = create_refresh_token(subject=user["email"])

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def delete_user(self, email: str):
        user = self.user_repo.find_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="유저를 찾을 수 없습니다."
            )
        if user.get("profile_image"):
            FileUtil.delete_file(user["profile_image"])

        self.user_repo.delete_by_email(email)

    async def update_user(self, email: str, update_data: UserUpdateRequest, profile_image: UploadFile | None):
        user = self.user_repo.find_by_email(email)
        #해당 하는 이메일의 사용자가 없을 시
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        #현재 비밀번호 검증
        if not verify_password(update_data.current_password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="현재 비밀번호가 일치하지 않습니다."
            )

        #current_password는 현재 비밀번호 검증을 위한 필드, password는 해시를 하여 저장하여야 하므로 따로 뺌
        update_dict = update_data.model_dump(exclude={"current_password","password"})

        # 일반 필드 업데이트 (nickname 등..)
        for key,value in update_dict.items():
            user[key] = value

        if update_data.password:
            # 새 비밀번호가 기존과 같은지 체크
            if verify_password(update_data.password, user["password"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="새 비밀번호는 이전과 달라야 합니다."
                )
            user["password"] = hash_password(update_data.password)

        if profile_image:
            if user.get("profile_image"):
                FileUtil.delete_file(user["profile_image"])

            new_image_path = await FileUtil.validate_and_save_image(profile_image)
            user["profile_image"] = new_image_path

        self.user_repo.save(user)
        return user

    async def find_user_by_id(self,id:int):
        target_user = self.user_repo.find_by_id(id)
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당하는 ID를 가진 유저를 찾을 수 없습니다."
            )

        return target_user


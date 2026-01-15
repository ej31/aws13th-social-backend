import os
import uuid
from datetime import datetime

from fastapi import HTTPException,status
from fastapi import UploadFile

from common.config import settings
from common.security import hash_password, encode_id, verify_password, create_access_token
from repositories.user_repository import UserRepository
from schemas.user import SignupRequest, UserLoginRequest

UPLOAD_DIR = settings.upload_dir

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class UserService:
    def __init__(self,user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def signup_user(self, signup_data: SignupRequest, profile_image: UploadFile | None):
        if self.user_repo.find_by_email(str(signup_data.email)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="해당 이메일은 이미 가입되었습니다.",
            )

        image_url = f"{settings.upload_dir}/default.png"
        if profile_image:
            if profile_image.content_type not in ["image/png","image/jpeg"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="JPG 또는 PNG 파일의 형식만 저장할 수 있습니다."
                )

            file_content = await profile_image.read()
            if len(file_content) > 5 * 1024 * 1024: #5MB
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="파일의 용량은 5MB를 넘을 수 없습니다."
                )

            file_name = f"{uuid.uuid4()}_{profile_image.filename}"
            file_path = os.path.join(UPLOAD_DIR, file_name)

            with open(file_path, "wb") as f:
                f.write(file_content)

            image_url = f"/{file_path}"

        user_id = self.user_repo.get_next_id()

        new_user = {
            "id": user_id,
            "email": signup_data.email,
            "nickname": signup_data.nickname,
            "password": hash_password(signup_data.password),
            "profile_image": image_url,
            "created_at": datetime.now().isoformat()
        }
        saved_user = self.user_repo.save(new_user)

        response_data = saved_user.copy()
        response_data["id"] = encode_id(saved_user["id"])

        return response_data

    async def login_user(self,login_data: UserLoginRequest):
        user = self.user_repo.find_by_email(str(login_data.email))

        #유저가 없거나 비밀번호가 틀렸을 경우
        if not user or not verify_password(login_data.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다."
            )

        access_token = create_access_token(subject=user["email"])

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    async def delete_user(self,email:str):
        user = self.user_repo.find_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="유저를 찾을 수 없습니다."
            )
        if user.get("profile_image"):
            self._delete_profile_image_file(user["profile_image"])

        self.user_repo.delete_by_email(email)

    def _delete_profile_image_file(self,file_path:str):
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print("파일이 정상적으로 삭제 되었습니다.")
            except Exception as e:
                print(f"파일 삭제 실패: {e}")
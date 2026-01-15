from fastapi import UploadFile, HTTPException,status

from common.config import settings
import uuid
import os

class FileUtil:
    ALLOWED_EXTENSIONS = ["image/png","image/jpeg","image/jpg"]
    MAX_FILE_SIZE = 5* 1024*1024 #5mb

    @classmethod
    async def validate_and_save_image(cls,file:UploadFile,folder:str = settings.upload_dir) -> str:
        if file.content_type not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="JPG 또는 PNG 형식의 파일만 업로드할 수 있습니다."
            )

        content = await file.read()

        if len(content) > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="5MB가 넘는 파일은 저장할 수 없습니다."
            )
        #현재 파일이 전부 읽혀서 포인터가 맨 뒤로 가있으므로 다시 포인터를 맨 앞으로 옮긴다.
        await file.seek(0)

        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = f"{uuid.uuid4()}_{file.filename}"
        full_path = os.path.join(folder,filename)

        with open(full_path,"wb") as f:
            f.write(content)

        return  f"/{full_path}"

    @staticmethod
    def delete_file(file_path: str):
        actual_path = file_path.lstrip("/")
        if os.path.exists(actual_path):
            os.remove(actual_path)



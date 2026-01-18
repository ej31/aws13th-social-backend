from fastapi import APIRouter, Form, UploadFile, File, status
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
import os
import shutil
import re
from PIL import Image
import io

from utils.data import load_data, save_data
from utils.auth import get_password_hash
from schemas.user import SignupResponse

router = APIRouter()

# 이미지 저장 경로 설정
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/signup", status_code=201, response_model=SignupResponse)
async def signup(
        email: str = Form(...),
        password: str = Form(...),
        nickname: str = Form(...),
        profileImage: Optional[UploadFile] = File(None)
):
    # --- 1. 유효성 검사 (Validation) ---
    validation_errors = []

    # 1-1. 이메일 형식 검사
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email):
        validation_errors.append({"field": "email", "issue": "이메일 형식이 아닙니다."})

    # 1-2. 비밀번호 검사 (8자 이상, 특수문자 포함)
    special_char_regex = r"[!@#$%^&*(),.?\":{}|<>]"
    if len(password) < 8 or not re.search(special_char_regex, password):
        validation_errors.append({"field": "password", "issue": "비밀번호는 8자 이상이어야 하며 특수문자를 포함해야 합니다."})

    # 1-3. 닉네임 검사 (1~13자)
    if not (1 <= len(nickname) <= 13):
        validation_errors.append({"field": "nickname", "issue": "닉네임은 1자 이상 13자 이하이어야 합니다."})

    # 1-4. 프로필 이미지 검사 (확장자, 500x500px 이상)
    if profileImage:
        filename = profileImage.filename
        ext = filename.split(".")[-1].lower() if "." in filename else ""

        # 확장자 체크
        if ext not in ["jpg", "jpeg", "png"]:
            validation_errors.append({"field": "profileImage", "issue": "확장자는 jpg, jpeg, png만 가능합니다."})
        else:
            # 사이즈 체크
            try:
                contents = await profileImage.read()
                img = Image.open(io.BytesIO(contents))
                if img.width < 500 or img.height < 500:
                    validation_errors.append({"field": "profileImage", "issue": "사이즈는 500x500px 이상만 가능합니다."})
                await profileImage.seek(0)  # 파일 포인터 초기화
            except Exception:
                validation_errors.append({"field": "profileImage", "issue": "유효하지 않은 이미지 파일입니다."})

    # 유효성 에러 발생 시 422 반환
    if validation_errors:
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "잘못된 형식의 값입니다.",
                    "details": validation_errors
                }
            }
        )

    # --- 2. 중복 검사 ---
    users = load_data("users.json")
    if any(u["email"] == email for u in users):
        return JSONResponse(
            status_code=409,
            content={
                "status": "error",
                "error": {
                    "code": "Conflict",
                    "message": "이미 존재하는 데이터가 있습니다.",
                    "details": [{"field": "email", "issue": "이미 가입된 이메일 주소입니다."}]
                }
            }
        )

    # --- 3. 데이터 저장 ---
    # ID 생성
    new_id = 1
    if users:
        new_id = max(u["id"] for u in users) + 1

    # 이미지 파일 저장
    image_url = None
    if profileImage:
        ext = profileImage.filename.split(".")[-1]
        safe_filename = f"{new_id}_{int(datetime.now().timestamp())}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profileImage.file, buffer)

        image_url = f"http://localhost:8000/static/uploads/{safe_filename}"

    # 사용자 객체 생성 (비밀번호 해싱 필수)
    new_user = {
        "id": new_id,
        "email": email,
        "password": get_password_hash(password),
        "nickname": nickname,
        "profileImage": image_url,
        "createdAt": datetime.now().isoformat()
    }

    # JSON 파일에 저장
    users.append(new_user)
    save_data("users.json", users)

    # 응답 반환
    return {
        "status": "success",
        "data": {
            "id": new_user["id"],
            "email": new_user["email"],
            "nickname": new_user["nickname"],
            "profileImage": new_user["profileImage"],
            "createdAt": new_user["createdAt"]
        }
    }
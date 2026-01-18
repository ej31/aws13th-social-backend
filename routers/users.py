import os
import shutil
import re
import io
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Form, UploadFile, File, status, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from email_validator import validate_email, EmailNotValidError

from utils.data import load_data, save_data
from utils.auth import get_password_hash, verify_password, create_access_token
from schemas.user import SignupResponse, UserLogin, LoginResponse

router = APIRouter(prefix="/users", tags=["users"])

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
    try:
        # [수정] 상단에 import 되어 있으므로 중복 import 제거함
        validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        validation_errors.append({"field": "email", "issue": "이메일 형식이 아닙니다."})

    # 1-2. 비밀번호 검사 (8자 이상, 특수문자 포함)
    special_char_regex = r"[!@#$%^&*(),.?\":{}|<>]"
    if len(password) < 8 or not re.search(special_char_regex, password):
        validation_errors.append({"field": "password", "issue": "비밀번호는 8자 이상이어야 하며 특수문자를 포함해야 합니다."})

    # 1-3. 닉네임 검사 (1~13자)
    if not (1 <= len(nickname) <= 13):
        validation_errors.append({"field": "nickname", "issue": "닉네임은 1자 이상 13자 이하이어야 합니다."})

    # 1-4. 프로필 이미지 검사 (확장자, 500x500px 이상)
    # [수정] 이미지가 있을 때만 검사하도록 들여쓰기(Indentation) 수정!
    if profileImage:
        filename = profileImage.filename
        # 확장자 체크 로직 (간단한 버전)
        if "." not in filename:
            validation_errors.append({"field": "profileImage", "issue": "파일 확장자가 없습니다."})
        else:
            ext = filename.split(".")[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                validation_errors.append({"field": "profileImage", "issue": "확장자는 jpg, jpeg, png만 가능합니다."})

        # 사이즈 및 실제 이미지 형식 체크
        try:
            contents = await profileImage.read()
            img = Image.open(io.BytesIO(contents))

            # PIL을 통한 포맷 재확인
            if img.format.lower() not in ['jpeg', 'png']:
                validation_errors.append({"field": "profileImage", "issue": "유효하지 않은 이미지 포맷입니다."})

            if img.width < 500 or img.height < 500:
                validation_errors.append({"field": "profileImage", "issue": "사이즈는 500x500px 이상만 가능합니다."})

            await profileImage.seek(0)  # [중요] 파일 포인터 초기화 (저장하기 위해)
        except (IOError, Image.UnidentifiedImageError):
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
        # 파일명 안전하게 생성
        ext = profileImage.filename.split(".")[-1]
        safe_filename = f"{new_id}_{int(datetime.now().timestamp())}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profileImage.file, buffer)

        # [중요] 윈도우 역슬래시(\) 문제를 방지하기 위해 URL 형식(/)으로 통일
        image_url = f"/static/uploads/{safe_filename}"

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


@router.post("/login", response_model=LoginResponse)
async def login(login_data: UserLogin):
    # 1. 데이터 로드
    users = load_data("users.json")

    # 2. 유저 찾기
    user = next((u for u in users if u["email"] == login_data.email), None)

    # 3. 인증 실패 처리
    if not user or not verify_password(login_data.password, user["password"]):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": "error",
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "인증 실패"
                }
            }
        )

    # 4. 토큰 발급
    access_token = create_access_token(data={"sub": user["email"]})

    # 5. 성공 응답
    return {
        "status": "success",
        "data": {
            "accessToken": access_token,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "nickname": user["nickname"]
            }
        }
    }
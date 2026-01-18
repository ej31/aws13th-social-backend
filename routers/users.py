import os
import shutil
import re
import io
from datetime import datetime
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Form, UploadFile, File, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from PIL import Image
from email_validator import validate_email, EmailNotValidError

from utils.data import load_data, save_data
from utils.auth import get_password_hash, verify_password, create_access_token, get_current_user
from schemas.user import (
    SignupResponse,
    UserLogin,
    LoginResponse,
    ProfileResponse,
    UpdateProfileResponse,
    PublicUserResponse
)

router = APIRouter(tags=["users"])

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
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    # 1. 데이터 로드
    users = load_data("users.json")

    user = next((u for u in users if u["email"] == form_data.username), None)

    # 3. 인증 실패 처리
    if not user or not verify_password(form_data.password, user["password"]):
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


@router.get("/users/me", response_model=ProfileResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "status": "success",
        "data": {
            "id": current_user["id"],
            "email": current_user["email"],
            "nickname": current_user["nickname"],
            "profileImage": current_user["profileImage"],

            "joinedAt": current_user["createdAt"]
        }
    }



@router.patch("/users/me", response_model=UpdateProfileResponse)
async def update_user_profile(
        nickname: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        profileImage: Optional[UploadFile] = File(None),
        current_user: dict = Depends(get_current_user)
):
    users = load_data("users.json")
    validation_errors = []


    # 1-1. 닉네임 검사
    if nickname is not None:
        if not (1 <= len(nickname) <= 13):
            validation_errors.append({"field": "nickname", "issue": "닉네임은 13자 이하이어야 합니다."})

    # 1-2. 비밀번호 검사
    if password is not None:
        special_char_regex = r"[!@#$%^&*(),.?\":{}|<>]"
        if len(password) < 8 or not re.search(special_char_regex, password):
            validation_errors.append({"field": "password", "issue": "비밀번호는 8자 이상이어야 합니다."})

    # 1-3. 프로필 이미지 검사
    if profileImage is not None:
        filename = profileImage.filename
        if "." not in filename:
            validation_errors.append({"field": "profileImage", "issue": "확장자가 없습니다."})
        else:
            ext = filename.split(".")[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                validation_errors.append({"field": "profileImage", "issue": "확장자는 jpg, jpeg, png만 가능합니다."})

        # 이미지 내용 검사
        try:
            contents = await profileImage.read()
            img = Image.open(io.BytesIO(contents))

            if img.format.lower() not in ['jpeg', 'png']:
                validation_errors.append({"field": "profileImage", "issue": "유효하지 않은 이미지 포맷입니다."})

            if img.width < 500 or img.height < 500:
                validation_errors.append({"field": "profileImage", "issue": "사이즈는 500x500px 이상만 가능합니다."})

            await profileImage.seek(0)  # 파일 포인터 초기화
        except Exception:
            validation_errors.append({"field": "profileImage", "issue": "유효하지 않은 이미지 파일입니다."})

    # 에러가 하나라도 있으면 422 리턴
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


    # 전체 유저 목록에서 현재 로그인한 유저 찾기 (수정하기 위해)
    user_idx = next((index for (index, u) in enumerate(users) if u["id"] == current_user["id"]), None)

    if user_idx is None:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "error": {"code": "NOT_FOUND", "message": "사용자를 찾을 수 없습니다."}}
        )

    # 2-1. 닉네임 업데이트
    if nickname:
        users[user_idx]["nickname"] = nickname

    # 2-2. 비밀번호 업데이트 (해싱 필수!)
    if password:
        users[user_idx]["password"] = get_password_hash(password)

    # 2-3. 이미지 업데이트
    if profileImage:
        ext = profileImage.filename.split(".")[-1]
        safe_filename = f"{users[user_idx]['id']}_{int(datetime.now().timestamp())}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profileImage.file, buffer)

        users[user_idx]["profileImage"] = f"/static/uploads/{safe_filename}"

    # --- 3. 저장 및 응답 ---
    save_data("users.json", users)
    updated_user = users[user_idx]

    return {
        "status": "success",
        "data": {
            "id": updated_user["id"],
            "nickname": updated_user["nickname"],
            "profileImage": updated_user["profileImage"],
            "createdAt": updated_user["createdAt"]
        }
    }


# [1] 회원 탈퇴 API
@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(current_user: dict = Depends(get_current_user)):

    users = load_data("users.json")

    # 현재 로그인한 유저(current_user["id"])를 제외한 나머지 리스트 생성
    new_users = [u for u in users if u["id"] != current_user["id"]]

    # 저장
    save_data("users.json", new_users)

    # 204 No Content는 본문(Body) 없이 상태 코드만 보냅니다.
    return


# [2] 특정 회원 조회 API
@router.get("/users/{user_id}", response_model=PublicUserResponse)
async def read_user_by_id(user_id: int):

    users = load_data("users.json")

    # 유저 찾기
    user = next((u for u in users if u["id"] == user_id), None)

    # 없으면 404 에러
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "error",
                "error": {
                    "code": "NOT_FOUND",
                    "message": "요청하신 데이터를 찾을 수 없습니다."
                }
            }
        )

    # 성공 시 공개 데이터 반환
    return {
        "status": "success",
        "data": {
            "id": user["id"],
            "nickname": user["nickname"],
            "profileImage": user["profileImage"]
        }
    }
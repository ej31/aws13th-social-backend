import time
import re
from typing import Annotated
from fastapi import FastAPI, HTTPException, Form, UploadFile, File, Body
from pydantic import EmailStr
from passlib.context import CryptContext

app = FastAPI()
#----- 데모용 DB (현재는 임시 리스트) ----------------------------
demo_db = []
#----- 비밀번호 규칙 -------------------------------------------
password_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*+=-]).{5,20}$"
def validate_password(password: str):
    if not re.match(password_pattern, password):
        raise HTTPException(
            status_code=422,
            detail="비밀번호는 5~20자 길이를 준수해야하며, 숫자, 영문 소문자, 영문 대문자, 특수 문자가 각각 최소 1개씩 포함되어야 합니다."
        )
#----- 비밀 번호 해싱 from JEFF --------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 1. 비밀번호 해싱
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
# 2 . 비밀번호 검증 (로그인 메서드에서 활용해야 함)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
#----- 닉네임 생성  -----------------------------------------
nickname_pattern = "^[a-zA-Z0-9가-힣].{5,10}$"

def validate_nickname(nickname: str):
    if not re.match(nickname_pattern, nickname):
        raise HTTPException(
            status_code=422,
            detail="닉네임은 5~10자 길이를 준수해야하며, 숫자, 영문 소문자, 영문 대문자, 한글을 사용할 수 있습니다. 중복 허용 불가입니다."
        )
#----- user_id 부여 (추후 DB 확장성 고려, 함수 형태로 구현)-------
user_counter = 0
def generate_user_id():
    global user_counter
    user_counter += 1
    return f"user_{user_counter}"
#----- 이미지 파일 용량 확인 ----------------------------------
ALLOWED_TYPES = {"image/jpg", "image/png", "image/tiff", "image/bmp", "image/gif"}
MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB
async def validate_image_size(upload_file):
    size = 0
    chunk_size = 1024 * 1024  # 1MB
    while True:
        chunk = await upload_file.read(chunk_size)
        if not chunk:
            break
        size += len(chunk)
        if size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="이미지 파일은 10MB를 넘을 수 없습니다. "
            )
    await upload_file.seek(0)

# ----- 첫번째. 회원 가입 메서드 시작
@app.post("/users")
async def post_users(
        email_address: Annotated[EmailStr, Form()],
        password: Annotated[str, Form()],
        nickname: Annotated[str, Form()],
        profile_image: Annotated[UploadFile | None, File()] = None
):
    # 이메일 중복 확인
    if any(user["email_address"] == email_address for user in demo_db):
        raise HTTPException(status_code=409, detail="해당 이메일은 이미 등록되어 있습니다.")
    # 비밀번호 규칙
    validate_password(password)
    # 비밀번호 해싱
    hashed_password = hash_password(password)
    # 닉네임 규칙
    validate_nickname(nickname)
    # 닉네임 중복 확인
    if any(user["nickname"] == nickname for user in demo_db):
        raise HTTPException(status_code=409, detail="해당 닉네임은 이미 등록되어 있습니다.")
    # 코드 리뷰 반영 --> 프로필 이미지 처리 로직 추가
    profile_image_url = None
    # 이미지 파일 확장자 검증
    if profile_image:
        if profile_image.content_type not in ALLOWED_TYPES:
            raise HTTPException(415, "지원하지 않는 이미지 파일 형식입니다. ")
        #TODO : 파일 저장 및 이미지 크기 확인 로직
        await validate_image_size(profile_image)
        profile_image_url = f"/uploads/{profile_image.filename}"
    # user_id 부여
    generate_user_id()
    # DB에 저장 -- 지금은 리스트에 임시로...
    demo_db.append({
        "email_address": email_address,
        "hashed_password": hashed_password,
        "nickname": nickname,
        "profile_image_url": profile_image_url
    })
    return {
        "status" : "success",
        "message" : "회원가입이 정상적으로 처리되었습니다.",
        "user_id"
        "email_address": email_address,
        "nickname": nickname,
        # 코드리뷰 반영 -->  UploadFile 객체 직접 반환 시 JSON 직렬화 에러 발생 방지
        "profile_image_url": profile_image if profile_image else None,
        "users_created_time" : time.strftime('%Y.%m.%d - %H:%M:%S')
    }

# ----- 두번째. 로그인 메서드 시작


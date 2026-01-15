import time, re
from typing import Annotated
from fastapi import FastAPI, Form, UploadFile, File, Header, HTTPException
from pydantic import EmailStr

api = FastAPI()
#----- 데모용 DB (현재는 임시 리스트) ----------------------------
demo_db = []
#----- 비밀번호 규칙 -------------------------------------------
password_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*+=-]).{5,20}$"
def validate_password(password: str):
    if not re.match(password_pattern, password):
        raise HTTPException(
            status_code=422,
            detail="비밀번호는 5~20자 길이를 준수해야하며, 숫자, 영문 소문자, 영문 대문자, 특수 문자가 각각 최소 1개씩 포함되어야 합니다."
        )
#----- 비밀 번호 해싱 from JEFF --------------------------------
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 1. 비밀번호 해싱
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
# 2 . 비밀번호 검증 (로그인 메서드에서 활용해야 함)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ----- 회원 가입 메서드 시작
@api.post("/users")
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
    # DB에 저장 -- 지금은 리스트에 임시로...
    demo_db.append({
        "email_address": email_address,
        "hashed_password": hashed_password,
        "nickname": nickname
    })
    return {
        "status" : "success",
        "message" : "회원가입이 정상적으로 처리되었습니다.",
        "email_address": email_address,
        "nickname": nickname,
        "profile_image_url": profile_image if profile_image else None,
        "users_created_time" : time.strftime('%Y.%m.%d - %H:%M:%S')
    }
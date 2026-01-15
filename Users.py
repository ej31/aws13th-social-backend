from typing import Annotated, Optional
from datetime import datetime, timezone, timedelta
import json,os,uuid
from fastapi import FastAPI, Form, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from jose import jwt

"""
Users리소스 유의사항
- 개발 편의상 비밀번호 생성의 검증규칙(대문자, 특수문자 등등)은 자릿수값(최소2자, 최대50자)만 체크하도록 간소화한다.
- 개발 편의상 요청으로 들어온 비밀번호는 평문화 한다.(원래는 요청값 전송 즉시 해쉬화 하고, 평문 비밀번호는 삭제)
- DB저장 로직을 제외함으로, 해쉬된 비밀번호 및 users의 필드는 저장되지 않는다.
- JWT토큰은 임의로 생성된 secret값을 가진다. 
- UUID사용 하여 users구분값인 무작위 user_id생성 이후 user_id로 토큰 생성
"""

#jwt토큰 검증 pydantic모델, 토큰 기본값은 2시간
class JwtSettings(BaseSettings):
    SECRET_KEY: str ="dev_secret_key"
    ALGORITHM: str ="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    model_config = SettingsConfigDict(env_file=".env")

settings = JwtSettings()
app = FastAPI()

class UsersBase(BaseModel):
    nickname :Annotated[Optional[str], Field(min_length=2, max_length=20, description="2자 이상 20자 이하의 닉네임")] = None
    email : Annotated[EmailStr, Field(description="사용자 이메일")]
    password : Annotated[str, Field(min_length=8, max_length=50)] # 비밀번호 복잡성 로직은 나중에 추가
    profile_image_url: Optional[HttpUrl] = None

    @classmethod
    def as_form(
            cls,
            email: Annotated[EmailStr, Form()],
            nickname: Annotated[str, Form()],
            password: Annotated[str, Form()],
            password_confirm: Annotated[str, Form()]
    ):
        if password != password_confirm:
            raise HTTPException(status_code=400, detail="패스워드 불일치")
        return cls(email=email,nickname=nickname, password=password)

class UserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user : UsersBase
    created_at: datetime


def create_access_token(user_id: str):
    now = datetime.now(timezone.utc)
    expire_at = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": expire_at
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    return token, expires_in



DB_FILE = "users.json"

def get_db_users():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_user_to_json(user_dict: dict):
    users = get_db_users()
    if any(u['email'] == user_dict['email'] for u in users):
        return False
    users.append(user_dict)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    return True

@app.post("/auth/signup",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def signup(form_data: Annotated[UsersBase, Depends(UsersBase.as_form)]):
    #user_id 생성
    user_id = str(uuid.uuid4())

    #db저장
    user_dict = form_data.model_dump()
    user_dict["user_id"] = user_id
    user_dict["created_at"] = datetime.now(timezone.utc).isoformat()

    if not save_user_to_json(user_dict):
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    token, expires_in = create_access_token(user_id)

    return UserResponse(
        access_token=token,
        token_type="bearer",
        expires_in=expires_in,
        user=form_data,
        created_at=datetime.now(timezone.utc)
    )


@app.post("/auth/login",response_model=UserResponse)
async def login(login_data : Annotated[UsersBase, Depends(UsersBase.as_form)]):
    users = get_db_users()
    user_record = next((u for u in users if u["email"] == login_data.email), None)
    token, expires_in = create_access_token(user_record["user_id"])

    return UserResponse(
        access_token=token,
        token_type="bearer",
        expires_in=expires_in,
        created_at=datetime.now(timezone.utc)
    )

# @app.post("/auth/logout")
# async def logout(user: Users):
#     return {"logout": user}

@app.get("/users/me",response_model=UserResponse)
async def get_users():
    return {"username": "admin", "email": "", "password": ""}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.patch("/users/me")
async def update_user(user_id: int):
    return {"user_id": user_id}

@app.delete("/users/me")
async def delete_user(user_id: int):
    return {"user_id": user_id}

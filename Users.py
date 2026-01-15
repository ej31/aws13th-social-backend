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
        """
            폼 데이터로부터 UsersBase 인스턴스를 생성한다.
            
            Parameters:
                email (EmailStr): 사용자 이메일 폼 값.
                nickname (str): 닉네임 폼 값.
                password (str): 비밀번호 폼 값.
                password_confirm (str): 비밀번호 확인 폼 값; `password`와 일치해야 함.
            
            Returns:
                UsersBase: 전달된 이메일, 닉네임, 비밀번호로 초기화된 모델 인스턴스.
            
            Raises:
                HTTPException: `password`와 `password_confirm`이 다르면 상태 코드 400과 메시지 "패스워드 불일치"로 발생.
            """
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
    """
    주어진 사용자 ID로 JWT 액세스 토큰을 생성한다.
    
    Parameters:
        user_id (str): 토큰의 `sub` 클레임에 설정할 사용자 고유 식별자.
    
    Returns:
        tuple: 인코딩된 JWT 문자열와 토큰 만료까지 남은 초 수. 첫 요소는 토큰(`str`), 두 번째 요소는 만료까지 남은 초(`int`).
    """
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
    """
    JSON 파일에서 사용자 목록을 로드하여 반환합니다.
    
    파일이 존재하면 DB_FILE에서 JSON을 읽어 파싱된 리스트를 반환합니다. 파일이 없거나 JSON 디코드 오류가 발생하면 빈 리스트를 반환합니다.
    
    Returns:
        list: DB_FILE에 저장된 사용자 레코드의 리스트, 없거나 파싱 불가한 경우 빈 리스트.
    """
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_user_to_json(user_dict: dict):
    """
    새 사용자 객체를 JSON 파일(DB_FILE)에 추가한다.
    
    Parameters:
        user_dict (dict): 저장할 사용자 데이터로, 적어도 'email' 키를 포함해야 한다.
    
    Returns:
        bool: 이메일이 기존에 등록되어 있지 않으면 `True`로 저장 성공을 나타내며, 이미 존재하면 `False`를 반환한다.
    """
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
    """
    새 사용자를 생성하고 저장한 뒤 액세스 토큰과 사용자 정보를 포함한 응답을 반환합니다.
    
    Parameters:
        form_data (UsersBase): 회원가입 폼 데이터(이메일, 비밀번호, 닉네임 등).
    
    Returns:
        UserResponse: 생성된 JWT 액세스 토큰(`access_token`), 토큰 타입(`token_type`), 만료까지 남은 초(`expires_in`), 저장된 사용자 정보(`user`), 응답 생성 시점의 UTC 타임스탬프(`created_at`)를 포함한 응답 모델.
    """
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
    """
    주어진 이메일로 저장된 사용자 레코드를 찾아 해당 사용자 ID로 JWT 액세스 토큰을 발급합니다.
    
    Parameters:
        login_data: 폼으로 전달된 사용자 로그인 데이터(이메일과 비밀번호). 이메일 필드를 사용해 저장된 사용자 레코드를 조회합니다.
    
    Returns:
        UserResponse: 발급된 `access_token`, 고정된 `token_type` "bearer", 만료까지의 초(`expires_in`), 그리고 토큰 발급 시각(`created_at`)을 포함한 응답 모델입니다.
    """
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
    """
    관리자 기본 사용자 정보를 반환합니다.
    
    Returns:
        dict: 사용자 정보 객체. 키는 `username`(관리자 이름, str), `email`(이메일 문자열, str), `password`(비어있을 수 있는 패스워드 문자열, str) 입니다.
    """
    return {"username": "admin", "email": "", "password": ""}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """
    지정한 사용자 ID를 포함한 간단한 사용자 정보를 반환합니다.
    
    Parameters:
        user_id (int): 조회할 사용자 식별자(경로 매개변수).
    
    Returns:
        dict: 키 `"user_id"`에 요청한 사용자 ID를 담은 사전.
    """
    return {"user_id": user_id}

@app.patch("/users/me")
async def update_user(user_id: int):
    """
    사용자 정보를 갱신하는 엔드포인트의 자리표시자 핸들러입니다.
    
    Returns:
        dict: 키 `user_id`에 전달된 사용자 ID(int)를 담은 응답 객체.
    """
    return {"user_id": user_id}

@app.delete("/users/me")
async def delete_user(user_id: int):
    """
    지정한 사용자 ID에 해당하는 사용자를 삭제하고 결과를 반환합니다.
    
    Parameters:
        user_id (int): 삭제할 사용자의 식별자.
    
    Returns:
        dict: 삭제된 사용자 ID를 포함한 딕셔너리, 예: {'user_id': <int>}.
    """
    return {"user_id": user_id}
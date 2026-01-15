from typing import Annotated, Optional
from datetime import datetime, timezone, timedelta
import json,os,uuid
from fastapi import Form, HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from jose import jwt, JWTError

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
    model_config = SettingsConfigDict(env_file="../.env")

settings = JwtSettings()

router = APIRouter(tags=["users"])

#공통 필드
class UserAuthBase(BaseModel):
    email: Annotated[EmailStr, Field(description="사용자 이메일")]
    password: Annotated[str, Field(min_length=8, max_length=50)]

class UsersBase(UserAuthBase):
    nickname :Annotated[Optional[str], Field(min_length=2, max_length=20, description="2자 이상 20자 이하의 닉네임")] = None
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

class LoginRequest(UserAuthBase):
    @classmethod
    def as_form(cls,
                email: Annotated[EmailStr, Form()],
                password: Annotated[str, Form()]):
        return cls(email=email, password=password)

class UserUpdate(BaseModel):
    # 수정하고 싶은 필드만 선택적으로 받을 수 있게 Optional 처리
    email: Annotated[Optional[EmailStr], Field(description="사용자 이메일")] = None
    password: Annotated[Optional[str], Field(min_length=8, max_length=50)] = None
    nickname: Annotated[Optional[str], Field(min_length=2, max_length=20)] = None
    profile_image_url: Optional[HttpUrl] = None

    @classmethod
    def as_form(
        cls,
        email: Optional[EmailStr] = Form(None),
        nickname: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        profile_image_url: Optional[HttpUrl] = Form(None)
    ):
        return cls(
            email=email,
            nickname=nickname,
            password=password,
            profile_image_url=profile_image_url
        )



class UserPublicResponse(BaseModel):
   nickname: Optional[str] = None
   email: EmailStr
   profile_image_url: Optional[HttpUrl] = None

class UserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user : UserPublicResponse
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

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload if payload.get("sub") else None
    except JWTError:
        return None

DB_FILE = "./users.json"
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="자격 증명을 확인 할 수 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    users = get_db_users()
    user = next((u for u in users if u["user_id"] == user_id), None)

    if user is None:
        raise credentials_exception

    return user

@router.post("/auth/signup",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
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
        user=UserPublicResponse(nickname=form_data.nickname, email=form_data.email, profile_image_url=form_data.profile_image_url),
        created_at=datetime.now(timezone.utc)
    )

@router.post("/auth/login",response_model=UserResponse)
async def login(
        # login_data: Annotated[LoginRequest, Depends(LoginRequest.as_form)]
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    users = get_db_users()
    user_record = next((u for u in users if u["email"] == login_data.username), None)

    if not user_record:
        raise HTTPException(status_code=401,detail="없는 유저입니다.")

    if not user_record or user_record["password"] != login_data.password:
        print(f"DB비번: {user_record['password']}, 입력비번: {login_data.password}")
        raise HTTPException(status_code=401, detail="인증 정보가 올바르지 않습니다.")

    token, expires_in = create_access_token(user_record["user_id"])

    return UserResponse(
        access_token=token,
        token_type="bearer",
        expires_in=expires_in,
        user=UserPublicResponse(**user_record),
        created_at=datetime.now(timezone.utc)
    )
@router.post("/auth/logout")
async def logout():
    return {"logout": "로그아웃 성공"}


@router.get("/users/me",response_model=UserPublicResponse)
async def get_user_me(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user

@router.get("/users/{user_id}", response_model=UserPublicResponse)
async def get_user(user_id: str):
    users = get_db_users()
    user =next((u for u in users if u["user_id"] == user_id),None)
    if user is None:
        raise HTTPException(status_code=404,detail="해당 사용자를 찾을수 없습니다")
    return UserPublicResponse(**user)

@router.patch("/users/me",response_model=UserPublicResponse)
async def update_user(
        update_data : Annotated[UserUpdate, Depends(UserUpdate.as_form)],
        current_user:  Annotated[dict, Depends(get_current_user)]):
    users = get_db_users()
    user =next((i for i,u in enumerate(users) if u["user_id"] == current_user["user_id"]),None)
    if user is None:
        raise HTTPException(status_code=404,detail="해당 유저가 없습니다")

    patch_dict = update_data.model_dump(exclude_unset=True,mode="json")

    users[user].update(patch_dict)

    with open(DB_FILE,"w",encoding="utf-8") as f:
        json.dump(users,f,ensure_ascii=False,indent=4)
    return users[user]

@router.delete("/users/me",status_code=status.HTTP_200_OK)
async def delete_user(current_user: Annotated[dict, Depends(get_user_me)]):
    users = get_db_users()

    # 2. 내 ID를 제외한 나머지 유저들만 필터링 (삭제 효과)
    original_count = len(users)
    users = [u for u in users if u["user_id"] != current_user["user_id"]]

    # 3. 만약 리스트 크기가 줄어들지 않았다면 삭제 실패
    if len(users) == original_count:
        raise HTTPException(status_code=404, detail="삭제할 유저를 찾을 수 없습니다.")

    # 4. ★ 핵심: 변경된 리스트를 다시 파일에 덮어쓰기
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

    return {"user_id": "삭제되었음"}

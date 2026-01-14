from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status, Depends

from schemas.user import UserCreate, UserResponse, Token, UserLogin
from utils import auth, data

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):

    existing_user = data.find_by_field("users.json", "email", user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일"
        )

    hashed_password = auth.hash_password(user_data.password)

    user_id = data.get_next_id("users.json")

    now = datetime.now(timezone.utc).isoformat()
    new_user = {
        "id": user_id,
        "email": user_data.email,
        "nickname": user_data.nickname,
        "profile_image": user_data.profile_image,
        "hashed_password": hashed_password,
        "created_at": now,
        "updated_at": now
    }

    users = data.load_data("users.json")
    users.append(new_user)
    success = data.save_data(users, "users.json")

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="사용자 생성에 실패"
        )

    # UserResponse 반환 (hashed_password 제외)
    return UserResponse(
        id=new_user["id"],
        email=new_user["email"],
        nickname=new_user["nickname"],
        profile_image=new_user["profile_image"],
        created_at=new_user["created_at"],
        updated_at=new_user["updated_at"]
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):

    user = data.find_by_field("users.json", "email", credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not auth.verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token_data = {
        "sub": user["email"],
        "user_id": user["id"]
    }
    access_token = auth.create_access_token(token_data)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(auth.get_current_user)):

    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        nickname=current_user["nickname"],
        profile_image=current_user.get("profile_image"),
        created_at=current_user["created_at"],
        updated_at=current_user["updated_at"]
    )



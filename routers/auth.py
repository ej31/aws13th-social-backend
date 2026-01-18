from fastapi import APIRouter, HTTPException
from schemas.users import UserLogin, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/tokens")
async def login(user: UserLogin):
    """로그인"""
    # TODO: 로그인 로직 구현
    raise HTTPException(status_code=501, detail="로그인 기능이 아직 구현되지 않았습니다.")

from fastapi import APIRouter, HTTPException
from schemas.users import UserLogin, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/tokens")
async def login(user: UserLogin):
    """로그인"""
    # TODO: 로그인 로직 구현
    return {
        "status": "success",
        "message": "로그인에 성공하였습니다.",
        "data": {
            "userId": 1,
            "nickname": "user",
            "accessToken": "token",
            "tokenType": "Bearer",
            "expiresIn": 3600
        }
    }
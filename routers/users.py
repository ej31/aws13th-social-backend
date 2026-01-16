from fastapi import APIRouter
from schemas.user import UserCreate

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate):
    return{
        "message": "회원가입 요청 받음",
        "data": user
    }
from fastapi import APIRouter
from schemas.user import UserCreate
from utils.data import load_data, save_data

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate):

    users = load_data("data/users.json")

    user_data = user.dict()

    users.append(user_data)

    save_data("data/users.json", users)

    return {"message": "회원가입 성공!", "data": user_data}
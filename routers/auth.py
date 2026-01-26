from typing import Annotated


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.config import pwd_context
from data.database import get_db
from schemas.Signup import SignupForm
from schemas.Login import  LoginForm
from core import config
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", status_code=201) #회원가입 스키마 연결
def signup(form: Annotated[SignupForm, Depends()], db : Session = Depends(get_db)):

    auth_service = AuthService(db, pwd_context, config)
    return auth_service.signup(form)


@router.post("/login") #로그인기능
def login(form: Annotated[LoginForm, Depends()], db : Session = Depends(get_db)):

    auth_service = AuthService(db, pwd_context, config)
    return auth_service.login(form.email, form.password)

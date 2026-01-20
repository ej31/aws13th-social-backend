from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from data.database import get_db
from data import models
from schemas.Signup import SignupForm

router = APIRouter(prefix="/auth", tags=["Auth"])

#회원가입 스키마 연결
@router.post("/signup")
def signup(form: SignupForm = Depends(), db : Session = Depends(get_db)): #의존성 주입... 개꿀인듯
    #이메일 중복 검증
    existed_email = db.query(models.User_data_base).filter(models.User_data_base.email == form.email).first()
    if existed_email:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
    #닉네임 중복 검증
    existed_nickname = db.query(models.User_data_base).filter(models.User_data_base.nickname == form.nickname).first()
    if existed_nickname:
        raise HTTPException(status_code=400, detail="이미 존재하는 닉네임입니다.")
    #검증 통과하면 새로 만들기
    new_user = models.User_data_base(email=form.email, password=form.password, nickname=form.nickname, profile_img=form.profile_image)

    return {
        "msg": "데이터 검증 성공!",
        "email": form.email,
        "password_len": len(form.password)  # 비밀번호는 그대로 보여주면 안 되니 길이만 확인
    }
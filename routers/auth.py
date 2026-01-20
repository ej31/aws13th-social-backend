from fastapi import APIRouter, Depends, HTTPException
from packaging.utils import parse_wheel_filename
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from data.database import get_db
from data import models
from schemas.Signup import SignupForm

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#회원가입 스키마 연결
@router.post("/signup")
def signup(form: SignupForm = Depends(), db : Session = Depends(get_db)): #의존성 주입... 개꿀인듯

    #이메일 중복 검증
    existed_email = db.query(models.User).filter(models.User.email == form.email).first()
    if existed_email:
        raise HTTPException(
            status_code=409, 
            detail={
                "code": "USERS_409_01",
                "message": "이미 존재하는 이메일입니다."
            }
        )

    #닉네임 중복 검증
    existed_nickname = db.query(models.User).filter(models.User.nickname == form.nickname).first()
    if existed_nickname:
        raise HTTPException(
            status_code=409,
            detail={
                "code" : "USERS_409_02",
                "message" : "이미 존재하는 닉네임입니다."
            }
        )
    #프로필 사진 검증
    if form.profile_image is not None:
        limit_size = 10 * 1024 * 1024
        if form.profile_image.size > limit_size:
            raise HTTPException(
                status_code=413,
                detail={
                    "code" : "UPLOAD_413_01",
                    "message" : "profile_image 10MB 초과"
                }
            )

        allowed_types = ["image/jpeg", "image/png", "image/jpg"]
        if form.profile_image.content_type not in allowed_types:
            raise HTTPException(
                status_code=415,
                detail={
                    "code" : "UPLOAD_415_02",
                    "message" : "Content-Type이 multipart/form-data가 아님"
                }
            )
    #검증 통과하면 새로 만들기
    new_user = models.User(email=form.email, password=pwd_context.hash(form.password), nickname=form.nickname, profile_img=form.profile_image)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "msg": "데이터 검증 성공!",
        "user_id": new_user.id,
        "email": new_user.email,
        "password_len": len(form.password)  # 비밀번호는 그대로 보여주면 안 되니 길이만 확인
    }

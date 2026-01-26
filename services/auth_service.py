from datetime import datetime, timedelta
from fastapi import HTTPException, UploadFile
from jose import jwt
from sqlalchemy.orm import Session

from data import models
from schemas.Signup import SignupForm


class AuthService:

    def __init__(self, db: Session, pwd_context,config):
        self.db = db
        self.user= models.User
        self.pwd_context = pwd_context
        self.config = config


    # 이메일 중복 검증 함수
    def validate_email_duplicate(self, email: str):
        if self.db.query(self.user).filter(self.user.email == email).first():
            raise HTTPException(
                status_code=409,
                detail={
                    "code": "USERS_409_01",
                    "message": "이미 존재하는 이메일입니다."
                }
            )

    # 이메일 존재 검증 함수
    def validate_email_exist(self,email: str):
        user = self.db.query(self.user).filter(self.user.email == email).first()
        if not user:
            raise HTTPException(
                status_code=401,
                detail={
                    "code": "AUTH_401_01",
                    "message": "이메일이 존재하지 않음(Invalid credentials)."
                }
            )
        return user

    # 비밀번호 검증 로직
    def verify_password(self,plain_password, hashed_password):
        verified_password=self.pwd_context.verify(plain_password, hashed_password)
        return verified_password


    # 닉네임 중복 검증 함수
    def validate_nickname_duplicate(self,nickname: str):
        if self.db.query(self.user).filter(self.user.nickname == nickname).first():
            raise HTTPException(
            status_code=409,
            detail={
                "code": "USERS_409_02",
                "message": "이미 존재하는 닉네임입니다."
            }
        )

    # 프로필 사진 검증 함수
    def validate_profile_image(self, profile_image: UploadFile | None):
        if profile_image is None:
            return None

        limit_size = 10 * 1024 * 1024
        if profile_image.size > limit_size:
            raise HTTPException(
                status_code=413,
                detail={
                    "code": "UPLOAD_413_01",
                    "message": "profile_image 10MB 초과"
                }
            )
        allowed_types = ["image/jpeg", "image/png", "image/jpg"]
        if profile_image.content_type not in allowed_types:
            raise HTTPException(
                status_code=415,
                detail={
                    "code": "UPLOAD_415_02",
                    "message": "Content-Type이 multipart/form-data가 아님"
                }
            )
        return profile_image

    # 새로운 유저 만드는 함수
    def create_user(self, form: SignupForm):
        hashed_password = self.pwd_context.hash(form.password)
        profile_img_path = form.profile_image.filename if form.profile_image else None

        new_user = self.user(
            email=form.email,
            password=hashed_password,
            nickname=form.nickname,
            profile_img=profile_img_path  # 파일 객체 말고 문자열(이름)을 넣어야 함!
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return {
        "msg": "데이터 검증 성공!",
        "user_id": new_user.id,
        "email": new_user.email,
        "password_len": len(form.password)
        }

    # 토큰 생성 로직
    def create_access_token(self,data: dict):

        to_encode = data.copy()

        # config 파일에서 유효기간 가져오기
        expire = datetime.utcnow() + datetime.timedelta(minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        # config 파일에서 비밀키, 알고리즘 가져오기
        encoded_jwt = jwt.encode(to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)

        return encoded_jwt


    #회원 가입 함수
    def signup(self, form: SignupForm):
        self.validate_email_duplicate(form.email)
        self.validate_nickname_duplicate(form.nickname)
        profile_image = self.validate_profile_image(form.profile_image)

        return self.create_user(form)

    #로그인 함수
    def login(self, email:str, password:str):
        user = self.validate_email_exist(email)
        if not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=401,
                detail={
                    "code": "AUTH_401_04",
                    "message": "이메일/비밀번호 불일치(Invalid credentials)."
                }
            )
        access_token = self.create_access_token({"sub": user.email})

        return {
            "status": "success",
            "data": {
                "email": user.email,
                "access_token": access_token,
                "token_type": "Bearer"
            }
        }






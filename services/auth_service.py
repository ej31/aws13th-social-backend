import uuid
from datetime import datetime,timezone

from core.db_connection import get_db_connection
from models.user import UserInternal
from repositories.user_repo import get_users
from services.jwt_service import create_access_token
from models.auth import UserSignUp, UserLogin
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password : str):
    return pwd_context.hash(password)

def verify_password(plain_password : str, hashed_password :str):
    return pwd_context.verify(plain_password, hashed_password)

def signup_user(data: UserSignUp):
    con = None
    try:
        con = get_db_connection()
        with con.cursor() as cursor:
            check_sql = "SELECT email FROM users WHERE email = %s"
            cursor.execute(check_sql, (data.email, ))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="이미 존재하는 이메일")

            hashed_password = get_password_hash(data.password)
            user_id = str(uuid.uuid4())
            user_created_at  = datetime.now(timezone.utc)

            insert_sql = "INSERT INTO users (user_id, email, password, nickname, profile_image_url, created_at) VALUES (%s, %s, %s, %s, %s, %s)"

            cursor.execute(insert_sql, (
                user_id,
                data.email,
                hashed_password,
                data.nickname,
                data.profile_image_url,
                user_created_at
            ))

            user=UserInternal(
                user_id=user_id,
                email=data.email,
                nickname=data.nickname,
                password=hashed_password,
                profile_image_url=data.profile_image_url,
                created_at=user_created_at
            )
        con.commit()
        token, expires = create_access_token(user.user_id)
        return user, token, expires
    except Exception :
        con.rollback()
        raise
    finally:
        if con :
            con.close()

def login_user(data: UserLogin):
    con = get_db_connection()
    try:
        with con.cursor() as cursor:
            check_sql = "SELECT user_id,email, password, nickname, profile_image_url FROM users where email = %s"
            cursor.execute(check_sql, (data.username,))
            user_record = cursor.fetchone()
            print(user_record)
            if user_record is None:
                raise HTTPException(status_code=401, detail="유저 정보(이메일 혹은 비밀번호)가 없습니다.")

            if not verify_password(data.password, user_record["password"]):
                raise HTTPException(401, "인증 실패")

            token, expires = create_access_token(user_record["user_id"])
            return user_record, token, expires
    except Exception as ex:
        con.rollback()
        raise ex
    finally:
        con.close()
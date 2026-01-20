import json

import bcrypt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr


app = FastAPI()


# BaseModel을 받은 데이터 모델 생성
class User(BaseModel):
    email: EmailStr
    password: str

    def hash_password(password: str):
        password_bytes = password.encode('utf-8')
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_bytes.decode('utf-8')


class Reader:

    def compare(self, input_data):
        with open('data/users.json', 'r') as f:
            read_json = json.load(f)

            u = input_data.email
            p = input_data.password
            hash_p = p.encode('utf-8')

            for info in read_json:
                if u == info['email']:
                    # ✅ CRITICAL FIX: bcrypt는 bytes 필요 (JSON은 보통 str)
                    stored_hash = info['password'].encode('utf-8')

                    if bcrypt.checkpw(hash_p, stored_hash):  # ✅ bytes, bytes
                        print("로그인 성공")
                        return "로그인 성공."

                    print("잘못된 이메일 또는 패스워드를 입력하셨습니다")
                    raise HTTPException(detail="잘못된 이메일 또는 패스워드를 입력하셨습니다.", status_code=400)

            return input_data


@app.post("/users/login", status_code=200)
def login_user(user: User):
    reader = Reader()
    input_data = reader.compare(user)
    return input_data


class UserCheck:
    with open('data/users.json', 'r') as f:
        users = json.load(f)
        email_list = []

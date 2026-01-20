import json
from datetime import datetime
import bcrypt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr




app = FastAPI()



# BaseModel을 받은 데이터 모델 생성
class User(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    profileImage: str | None = None

    def hash_password(password: str):
        password_bytes = password.encode('utf-8')
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_bytes.decode('utf-8')






@app.post("/users/signup", status_code=201)
def signup(user: User):
    with open ('data/users.json', 'r', encoding='utf-8') as f:

        try: users = json.load(f)

        except: users = []

    for e in users:
        if e['email'] == user.email:

            raise HTTPException(detail="이미 등록된 이메일 주소입니다.", status_code=400)

        print("사용 가능한 이메일입니다.")


    if len(users) == 0:
        new_id = 1

    elif len(users) > 0:
        last_user = users[-1]
        new_id = last_user['userId'] + 1

    hashed_pw = User.hash_password(user.password)
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    new_user_data = {
        "userId": new_id,
        "email": user.email,
        "nickname": user.nickname,
        "password": hashed_pw,
        "profileImage": user.profileImage,
        "createdAt": now
    }


    users.append(new_user_data)

    with open ('data/users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

    return {
        "status": "success",
        "data": {
            "userId": new_id,
            "email": user.email,
            "nickname": user.nickname,
            "createdAt": now
        }
    }
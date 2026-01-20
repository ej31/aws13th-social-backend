import json
import os
from datetime import datetime, timedelta
from json import JSONDecodeError
import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # 추가

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    profileImage: str | None = None


def hash_password(password: str):
    password_bytes = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="토큰 정보가 올바르지 않습니다.")
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
    except:
        users = []

    target_user = None
    for user in users:
        if user['email'] == email:
            target_user = user
            break

    if target_user is None:
        raise HTTPException(status_code=401, detail="삭제되었거나 존재하지 않는 회원입니다.")

    return target_user




# 회원가입
@app.post("/users/signup", status_code=201)
def signup(user: User):
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    for e in users:
        if e['email'] == user.email:
            raise HTTPException(detail="이미 등록된 이메일 주소입니다.", status_code=400)

    if len(users) == 0:
        new_id = 1
    else:
        last_user = users[-1]
        new_id = last_user['userId'] + 1

    hashed_pw = hash_password(user.password)
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

    with open('data/users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

    return {
        "status": "success",
        "data": {
            "userId": new_id,
            "email": user.email,
            "nickname": user.nickname,
            "createdAt": now
        }
    }


# 로그인
class Reader:
    def compare(self, input_data):
        try:
            with open('data/users.json', 'r', encoding='utf-8') as f:
                read_json = json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            raise HTTPException(status_code=400, detail="회원 정보 없습니다.")

        u = input_data.email
        p = input_data.password
        hash_p = p.encode('utf-8')

        for info in read_json:
            if u == info['email']:
                stored_hash = info['password'].encode('utf-8')

                if bcrypt.checkpw(hash_p, stored_hash):
                    jwt_token = create_access_token(data={"sub": u})
                    print("로그인 성공")
                    return {"access_token": jwt_token, "token_type": "bearer"}

                print("잘못된 이메일 또는 패스워드를 입력하셨습니다")
                raise HTTPException(detail="잘못된 이메일 또는 패스워드를 입력하셨습니다.", status_code=400)

        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못되었습니다.")


@app.post("/users/login", status_code=200)
def login_user(user: UserLogin):
    reader = Reader()
    input_data = reader.compare(user)
    return input_data



@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "userId": current_user["userId"],
        "email": current_user["email"],
        "nickname": current_user["nickname"],
        "profileImage": current_user.get("profileImage")
    }


# 프로필 수정 기능
class UserUpdate(BaseModel):
    nickname: str | None = None
    profileImage: str | None = None
    password: str | None = None


@app.patch("/users/me")
def update_user_me(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
    except:
        raise HTTPException(status_code=500, detail="데이터 오류")

    for u in users:
        if u['email'] == current_user['email']:
            if user_update.nickname is not None:
                u['nickname'] = user_update.nickname
            if user_update.profileImage is not None:
                u['profileImage'] = user_update.profileImage
            if user_update.password is not None:
                u['password'] = hash_password(user_update.password)

            with open('data/users.json', 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=4, ensure_ascii=False)

            return {"status": "success", "data": u}

    return {"status": "error", "message": "수정 실패"}


# 여기까지 프로필 수정


# 회원 탈퇴 기능
@app.delete("/users/me")
def delete_user_me(current_user: dict = Depends(get_current_user)):
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
    except:
        return {"msg": "삭제 실패"}

    new_users = []
    for u in users:
        if u['email'] != current_user['email']:
            new_users.append(u)

    with open('data/users.json', 'w', encoding='utf-8') as f:
        json.dump(new_users, f, indent=4, ensure_ascii=False)

    return {"status": "success", "message": "회원 탈퇴 완료"}


# 여기까지 회원 탈퇴


# 특정 회원 조회 기능
@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
    except:
        users = []

    for u in users:
        if u['userId'] == user_id:
            return {
                "userId": u['userId'],
                "email": u['email'],
                "nickname": u['nickname'],
                "profileImage": u.get("profileImage")
            }

    raise HTTPException(status_code=404, detail="유저 없음")


# 여기까지 특정 회원 조회


# 게시글 작성 기능
class PostCreate(BaseModel):
    title: str
    content: str


@app.post("/posts")
def create_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    if not os.path.exists('data'):
        os.makedirs('data')

    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        posts = []

    if len(posts) == 0:
        new_id = 1
    else:
        new_id = posts[-1]['id'] + 1

    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    new_post = {
        "id": new_id,
        "title": post.title,
        "content": post.content,
        "writerId": current_user['userId'],
        "writerNickname": current_user['nickname'],
        "views": 0,
        "likes": 0,
        "createdAt": now
    }

    posts.append(new_post)

    with open('data/posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

    return {"status": "success", "data": new_post}


# 여기까지 게시글 작성


# 게시글 목록 조회 기능
@app.get("/posts")
def get_posts(page: int = 1, keyword: str | None = None, sort: str | None = None):
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except:
        posts = []

    if keyword:
        filtered_posts = []
        for p in posts:
            if keyword in p['title'] or keyword in p['content']:
                filtered_posts.append(p)
        posts = filtered_posts

    if sort == "views":
        posts.sort(key=lambda x: x['views'], reverse=True)
    else:
        posts.sort(key=lambda x: x['id'], reverse=True)

    limit = 5
    start_index = (page - 1) * limit
    end_index = start_index + limit

    result_posts = posts[start_index:end_index]

    return {
        "total": len(posts),
        "page": page,
        "data": result_posts
    }


# 여기까지 게시글 목록 조회


# 게시글 상세 조회 기능
@app.get("/posts/{post_id}")
def get_post_detail(post_id: int):
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except:
        posts = []

    target_post = None

    for p in posts:
        if p['id'] == post_id:
            p['views'] = p['views'] + 1
            target_post = p
            break

    if target_post is None:
        raise HTTPException(status_code=404, detail="게시글 없음")

    with open('data/posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

    return target_post
# 여기까지 게시글 상세 조회

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

# 게시글 수정
@app.patch("/posts/{post_id}")
def patch_post_detail(
        post_id: int,
        post_update: PostUpdate,
        current_user: dict = Depends(get_current_user)
):
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except:
        raise HTTPException(status_code=500, detail="데이터를 읽을 수 없습니다.")

    target_post = None

    for p in posts:
        if p['id'] == post_id:
            target_post = p
            break
    if target_post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if target_post['writerId'] != current_user['userId']:
        raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")
    if post_update.title is not None:
        target_post['title'] = post_update.title

    if post_update.content is not None:
        target_post['content'] = post_update.content
    with open('data/posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

    return {"status": "success", "data": target_post}



# 여기까지 게시글 수정



# 게시글 삭제
@app.delete("/posts/{post_id}")
def delete_post(post_id: int, current_user: dict = Depends(get_current_user)):

    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except:
        raise HTTPException(status_code=500, detail="데이터를 읽을 수 없습니다.")
    target_post = None

    for p in posts:
        if p['id'] == post_id:
            target_post = p
            break

    if target_post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if target_post['writerId'] != current_user['userId']:
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")

    posts.remove(target_post)

    with open('data/posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

    return {"status": "success", "message": "게시글이 삭제되었습니다."}


# 여기까지 게시글 삭제



# 댓글 목록 조회
app.get("posts/{postId}/comments")
def comments_list():

    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            comments = json.load(f)
    except:
        comments = []

    target_comments = None

    for p in posts:
        if p['id'] == post_id:
            p['views'] = p['views'] + 1
            target_comments = p
            break

    if target_comments is None:
        raise HTTPException(status_code=404, detail="게시글 없음")

    with open('data/posts.json', 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=4, ensure_ascii=False)

    return target_comments


# 여기까지 댓글 목록 조회





# 댓글 작성
@app.post("/posts/{postId}/comments")
def create_comment(comment: commentCreate, current_user: dict = Depends(get_current_user)):
    if not os.path.exists('data'):
        os.makedirs('data')

    try:
        with open('data/comment.json', 'r', encoding='utf-8') as f:
            comments = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        comments = []

    if len(comments) == 0:
        new_id = 1
    else:
        new_id = comments[-1]['id'] + 1

    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    new_comment = {
        "id": new_id,
        "content": comment.content,
        "postId": get_posts['postId'],
        "writerId": current_user['userId'],
        "writerNickname": current_user['nickname'],
        "likes": 0,
        "createdAt": now
    }

    comments.append(new_comment)

    with open('data/comments.json', 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=4, ensure_ascii=False)

    return {"status": "success", "data": new_comment}



# 여기까지 댓글 작성



# 댓글 수정
@app.patch("/comments/{commentId}")
def patch_comment():
    comment_Id: int,
    comment_update: commentUpdate,
    current_user: dict = Depends(get_current_user)

    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
        comments = json.load(f)
    except:
        raise HTTPException(status_code=500, detail="데이터를 읽을 수 없습니다.")

    target_comment = None

for p in comments:
    if p['id'] == comment_id:
        target_post = p
        break
if target_post is None:
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
if target_post['writerId'] != current_user['userId']:
    raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")
if post_update.title is not None:
    target_post['title'] = post_update.title

if post_update.content is not None:
    target_post['content'] = post_update.content
    with open('data/posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

    return {"status": "success", "data": target_post}






import json
import os
from datetime import datetime, timedelta, timezone
from json import JSONDecodeError
import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
POSTS_FILE = os.path.join(DATA_DIR, "posts.json")
COMMENTS_FILE = os.path.join(DATA_DIR, "comments.json")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

app = FastAPI()
security = HTTPBearer()

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    profileImage: str | None = None

class UserUpdate(BaseModel):
    nickname: str | None = None
    profileImage: str | None = None
    password: str | None = None


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: str | None = None

def load_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        return []

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def hash_password(password: str):
    password_bytes = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')




def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="잘못된 토큰 정보입니다.")
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    users = load_data(USERS_FILE)

    target_user = None
    for u in users:
        if u['email'] == email:
            target_user = u
            break

    if target_user is None:
        raise HTTPException(status_code=401, detail="존재하지 않는 회원입니다.")

    return target_user


# Users
@app.post("/users/signup", status_code=201)
def signup(user: User):
    users = load_data(USERS_FILE)

    for u in users:
        if u['email'] == user.email:
            raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")

    if not users:
        new_id = 1
    else:
        new_id = users[-1]['userId'] + 1

    hashed_pw = hash_password(user.password)
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    new_user_data = {
        "userId": new_id,
        "email": user.email,
        "nickname": user.nickname,
        "password": hashed_pw,
        "profileImage": user.profileImage,
        "createdAt": now
    }

    users.append(new_user_data)
    save_data(USERS_FILE, users)

    return {
        "status": "success",
        "data": {
            "userId": new_id,
            "email": user.email,
            "nickname": user.nickname,
            "createdAt": now
        }
    }


@app.post("/users/login", status_code=200)
def login_user(user: UserLogin):
    users = load_data(USERS_FILE)

    target_user = None
    for u in users:
        if u['email'] == user.email:
            target_user = u
            break

    if target_user:
        is_pw_correct = bcrypt.checkpw(
            user.password.encode('utf-8'),
            target_user['password'].encode('utf-8')
        )
        if is_pw_correct:
            jwt_token = create_access_token(data={"sub": target_user['email']})
            return {"access_token": jwt_token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="이메일 또는 비밀번호 불일치")


@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "userId": current_user["userId"],
        "email": current_user["email"],
        "nickname": current_user["nickname"],
        "profileImage": current_user.get("profileImage")
    }


@app.patch("/users/me")
def update_user_me(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    users = load_data(USERS_FILE)

    target_index = -1
    for i, u in enumerate(users):
        if u['email'] == current_user['email']:
            target_index = i
            break

    if target_index == -1:
        raise HTTPException(status_code=404, detail="유저 정보를 찾을 수 없습니다.")

    user_data = users[target_index]

    if user_update.nickname is not None:
        user_data['nickname'] = user_update.nickname
    if user_update.profileImage is not None:
        user_data['profileImage'] = user_update.profileImage
    if user_update.password is not None:
        user_data['password'] = hash_password(user_update.password)

    users[target_index] = user_data
    save_data(USERS_FILE, users)

    return {"status": "success", "data": user_data}


@app.delete("/users/me")
def delete_user_me(current_user: dict = Depends(get_current_user)):
    users = load_data(USERS_FILE)

    new_users = [u for u in users if u['email'] != current_user['email']]

    if len(users) == len(new_users):
        return {"msg": "삭제에 실패하였습니다."}

    save_data(USERS_FILE, new_users)
    return {"status": "success", "message": "회원 탈퇴 완료"}


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    users = load_data(USERS_FILE)

    for u in users:
        if u['userId'] == user_id:
            return {
                "userId": u['userId'],
                "email": u['email'],
                "nickname": u['nickname'],
                "profileImage": u.get("profileImage")
            }

    raise HTTPException(status_code=404, detail="유저 없음")


@app.get("/users/me/posts")
def get_my_posts(current_user: dict = Depends(get_current_user)):
    posts = load_data(POSTS_FILE)

    my_posts = [p for p in posts if p['writerId'] == current_user['userId']]
    my_posts.sort(key=lambda x: x['id'], reverse=True)

    return {"count": len(my_posts), "data": my_posts}


# 여기까지 Users




# Posts
@app.post("/posts")
def create_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    posts = load_data(POSTS_FILE)

    if not posts:
        new_id = 1
    else:
        new_id = posts[-1]['id'] + 1

    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

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
    save_data(POSTS_FILE, posts)

    return {"status": "success", "data": new_post}


@app.get("/posts")
def get_posts(page: int = 1, keyword: str | None = None, sort: str | None = None):
    posts = load_data(POSTS_FILE)

    if keyword:
        posts = [p for p in posts if keyword in p['title'] or keyword in p['content']]

    if sort == "views":
        posts.sort(key=lambda x: x['views'], reverse=True)
    else:
        posts.sort(key=lambda x: x['id'], reverse=True)

    limit = 5
    start_index = (page - 1) * limit
    end_index = start_index + limit

    result_posts = posts[start_index:end_index]

    return {"total": len(posts), "page": page, "data": result_posts}


@app.get("/posts/{post_id}")
def get_post_detail(post_id: int):
    posts = load_data(POSTS_FILE)

    target_post = None
    target_index = -1

    for i, p in enumerate(posts):
        if p['id'] == post_id:
            target_post = p
            target_index = i
            break

    if target_post is None:
        raise HTTPException(status_code=404, detail="게시글이 없습니다.")

    target_post['views'] += 1
    posts[target_index] = target_post
    save_data(POSTS_FILE, posts)

    return target_post


@app.patch("/posts/{post_id}")
def patch_post_detail(
        post_id: int,
        post_update: PostUpdate,
        current_user: dict = Depends(get_current_user)
):
    posts = load_data(POSTS_FILE)

    target_post = None
    target_index = -1

    for i, p in enumerate(posts):
        if p['id'] == post_id:
            target_post = p
            target_index = i
            break

    if target_post is None:
        raise HTTPException(status_code=404, detail="게시글이 없습니다.")

    if target_post['writerId'] != current_user['userId']:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    if post_update.title is not None:
        target_post['title'] = post_update.title
    if post_update.content is not None:
        target_post['content'] = post_update.content

    posts[target_index] = target_post
    save_data(POSTS_FILE, posts)

    return {"status": "success", "data": target_post}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, current_user: dict = Depends(get_current_user)):
    posts = load_data(POSTS_FILE)

    target_post = None
    for p in posts:
        if p['id'] == post_id:
            target_post = p
            break

    if target_post is None:
        raise HTTPException(status_code=404, detail="게시글이 없습니다")

    if target_post['writerId'] != current_user['userId']:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    posts.remove(target_post)
    save_data(POSTS_FILE, posts)

    return {"status": "success", "message": "삭제 완료"}

# 여기까지 Posts



# Comments
@app.get("/posts/{post_id}/comments")
def get_comments(post_id: int):
    comments = load_data(COMMENTS_FILE)

    post_comments = [c for c in comments if c['postId'] == post_id]

    return {"count": len(post_comments), "data": post_comments}


@app.post("/posts/{post_id}/comments")
def create_comment(
        post_id: int,
        comment: CommentCreate,
        current_user: dict = Depends(get_current_user)
):
    comments = load_data(COMMENTS_FILE)

    if not comments:
        new_id = 1
    else:
        new_id = comments[-1]['id'] + 1

    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    new_comment = {
        "id": new_id,
        "postId": post_id,
        "content": comment.content,
        "writerId": current_user['userId'],
        "writerNickname": current_user['nickname'],
        "createdAt": now
    }

    comments.append(new_comment)
    save_data(COMMENTS_FILE, comments)

    return {"status": "success", "data": new_comment}


@app.patch("/comments/{comment_id}")
def update_comment(
        comment_id: int,
        comment_update: CommentUpdate,
        current_user: dict = Depends(get_current_user)
):
    comments = load_data(COMMENTS_FILE)

    target_comment = None
    target_index = -1

    for i, c in enumerate(comments):
        if c['id'] == comment_id:
            target_comment = c
            target_index = i
            break

    if target_comment is None:
        raise HTTPException(status_code=404, detail="댓글이 없습니다.")

    if target_comment['writerId'] != current_user['userId']:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    if comment_update.content is not None:
        target_comment['content'] = comment_update.content

    comments[target_index] = target_comment
    save_data(COMMENTS_FILE, comments)

    return {"status": "success", "data": target_comment}


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, current_user: dict = Depends(get_current_user)):
    comments = load_data(COMMENTS_FILE)

    target_comment = None
    for c in comments:
        if c['id'] == comment_id:
            target_comment = c
            break

    if target_comment is None:
        raise HTTPException(status_code=404, detail="댓글이 없습니다.")

    if target_comment['writerId'] != current_user['userId']:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    comments.remove(target_comment)
    save_data(COMMENTS_FILE, comments)

    return {"status": "success", "message": "삭제 완료"}



@app.get("/users/me/comments")
def get_user_comments(current_user: dict = Depends(get_current_user)):
    comments = load_data(COMMENTS_FILE)

    my_comm = []
    for i in comments:
        if i['writerId'] == current_user['userId']:
            my_comm.append(i)
    return
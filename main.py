import json
import os
from datetime import datetime, timedelta, timezone
from json import JSONDecodeError
from typing import Optional
import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr

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
    profileImage: Optional[str] = None

class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    profileImage: Optional[str] = None
    password: Optional[str] = None

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: Optional[str] = None

def load_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        return []

def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")

def create_access_token(data):
    to_encode = {}
    for k in data:
        to_encode[k] = data[k]

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire

    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="SECRET_KEY 설정 X")

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="잘못된 토큰 정보입니다.")
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    users = load_data(USERS_FILE)
    target_user = None
    for u in users:
        if u.get("email") == email:
            target_user = u
            break

    if target_user is None:
        raise HTTPException(status_code=401, detail="존재하지 않는 회원입니다.")

    return target_user

def sort_desc_by_int_key(items, key_name):

    n = len(items)
    i = 0
    while i < n:
        j = i + 1
        while j < n:
            left = items[i].get(key_name, 0)
            right = items[j].get(key_name, 0)
            if right > left:
                temp = items[i]
                items[i] = items[j]
                items[j] = temp
            j += 1
        i += 1

# Users
@app.post("/users/signup", status_code=201)
def signup(user: User):
    users = load_data(USERS_FILE)

    for u in users:
        if u.get("email") == user.email:
            raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")

    if len(users) == 0:
        new_id = 1
    else:
        new_id = users[-1].get("userId", 0) + 1

    hashed_pw = hash_password(user.password)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

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
        if u.get("email") == user.email:
            target_user = u
            break

    if target_user is not None:
        is_pw_correct = bcrypt.checkpw(
            user.password.encode("utf-8"),
            target_user.get("password", "").encode("utf-8")
        )

        if is_pw_correct:
            jwt_token = create_access_token({"sub": target_user["email"]})
            return {"access_token": jwt_token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="이메일 또는 비밀번호 불일치")

@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "userId": current_user.get("userId"),
        "email": current_user.get("email"),
        "nickname": current_user.get("nickname"),
        "profileImage": current_user.get("profileImage")
    }

@app.patch("/users/me")
def update_user_me(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    users = load_data(USERS_FILE)

    target_index = -1
    for i in range(len(users)):
        if users[i].get("email") == current_user.get("email"):
            target_index = i
            break

    if target_index == -1:
        raise HTTPException(status_code=404, detail="유저 정보를 찾을 수 없습니다.")

    user_data = users[target_index]

    if user_update.nickname is not None:
        user_data["nickname"] = user_update.nickname
    if user_update.profileImage is not None:
        user_data["profileImage"] = user_update.profileImage
    if user_update.password is not None:
        user_data["password"] = hash_password(user_update.password)

    users[target_index] = user_data
    save_data(USERS_FILE, users)

    return {"status": "success", "data": user_data}

@app.delete("/users/me")
def delete_user_me(current_user: dict = Depends(get_current_user)):
    users = load_data(USERS_FILE)

    new_users = []

    deleted = False

    for u in users:
        if u.get("email") == current_user.get("email"):
            deleted = True
        else:


            new_users.append(u)

    if not deleted:


        return {"msg": "삭제에 실패하였습니다."}

    save_data(USERS_FILE, new_users)

    return {"status": "success", "message": "회원 탈퇴 완료"}

@app.get("/users/me/posts")
def get_my_posts(current_user: dict = Depends(get_current_user)):
    posts = load_data(POSTS_FILE)

    my_posts = []
    for p in posts:
        if p.get("writerId") == current_user.get("userId"):
            my_posts.append(p)

    sort_desc_by_int_key(my_posts, "id")
    return {"count": len(my_posts), "data": my_posts}

@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    users = load_data(USERS_FILE)

    for u in users:

        if u.get("userId") == user_id:

            return {

                "userId": u.get("userId"),
                "email": u.get("email"),
                "nickname": u.get("nickname"),
                "profileImage": u.get("profileImage")
            }



    raise HTTPException(status_code=404, detail="유저 없음")



# 여기까지 Users

# Posts

@app.post("/posts")
def create_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    posts = load_data(POSTS_FILE)

    if len(posts) == 0:
        new_id = 1
    else:
        new_id = posts[-1].get("id", 0) + 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    new_post = {
        "id": new_id,
        "title": post.title,
        "content": post.content,
        "writerId": current_user.get("userId"),
        "writerNickname": current_user.get("nickname"),
        "views": 0,
        "likes": 0,
        "createdAt": now
    }

    posts.append(new_post)
    save_data(POSTS_FILE, posts)

    return {"status": "success", "data": new_post}

@app.get("/posts")
def get_posts(page: int = 1, keyword: Optional[str] = None, sort: Optional[str] = None):
    posts = load_data(POSTS_FILE)

    filtered = []
    if keyword is None:
        filtered = posts
    else:
        for p in posts:
            title = p.get("title", "")
            content = p.get("content", "")
            if (keyword in title) or (keyword in content):
                filtered.append(p)

    if sort == "views":
        sort_desc_by_int_key(filtered, "views")
    else:
        sort_desc_by_int_key(filtered, "id")

    limit = 5
    start_index = (page - 1) * limit
    end_index = start_index + limit
    result_posts = []
    idx = start_index
    while idx < end_index and idx < len(filtered):
        result_posts.append(filtered[idx])
        idx += 1

    return {"total": len(filtered), "page": page, "data": result_posts}

@app.get("/posts/{post_id}")
def get_post_detail(post_id: int):
    posts = load_data(POSTS_FILE)
    target_post = None
    target_index = -1

    for i in range(len(posts)):
        if posts[i].get("id") == post_id:
            target_post = posts[i]
            target_index = i
            break

    if target_post is None:
        raise HTTPException(status_code=404, detail="게시글이 없습니다.")

    target_post["views"] = target_post.get("views", 0) + 1
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

    for i in range(len(posts)):
        if posts[i].get("id") == post_id:
            target_post = posts[i]
            target_index = i
            break

    if target_post is None:
        raise HTTPException(status_code=404, detail="게시글이 없습니다.")

    if target_post.get("writerId") != current_user.get("userId"):
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    if post_update.title is not None:
        target_post["title"] = post_update.title
    if post_update.content is not None:
        target_post["content"] = post_update.content

    posts[target_index] = target_post
    save_data(POSTS_FILE, posts)

    return {"status": "success", "data": target_post}

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, current_user: dict = Depends(get_current_user)):
    posts = load_data(POSTS_FILE)

    target_index = -1
    for i in range(len(posts)):
        if posts[i].get("id") == post_id:
            target_index = i
            break

    if target_index == -1:
        raise HTTPException(status_code=404, detail="게시글이 없습니다")

    if posts[target_index].get("writerId") != current_user.get("userId"):
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    posts.pop(target_index)
    save_data(POSTS_FILE, posts)
    return {"status": "success", "message": "삭제 완료"}

# 여기까지 Posts
# Comments

@app.get("/posts/{post_id}/comments")
def get_comments(post_id: int):
    comments = load_data(COMMENTS_FILE)

    post_comments = []
    for c in comments:
        if c.get("postId") == post_id:
            post_comments.append(c)

    return {"count": len(post_comments), "data": post_comments}

@app.post("/posts/{post_id}/comments")
def create_comment(
    post_id: int,
    comment: CommentCreate,
    current_user: dict = Depends(get_current_user)
):



    def post_exists(post_id):
        posts = load_data(POSTS_FILE)

        if len(posts) == 0:
            raise HTTPException(status_code=404, detail="게시글이 없습니다.")

        for p in posts:
            if p.get("id") == post_id:
                return

        raise HTTPException(status_code=404, detail="게시글이 없습니다.")

    post_exists(post_id)

    comments = load_data(COMMENTS_FILE)

    if len(comments) == 0:
        new_id = 1
    else:
        new_id = comments[-1].get("id", 0) + 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    new_comment = {
        "id": new_id,
        "postId": post_id,
        "content": comment.content,
        "writerId": current_user.get("userId"),
        "writerNickname": current_user.get("nickname"),
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

    for i in range(len(comments)):
        if comments[i].get("id") == comment_id:
            target_comment = comments[i]
            target_index = i
            break

    if target_comment is None:
        raise HTTPException(status_code=404, detail="댓글이 없습니다.")

    if target_comment.get("writerId") != current_user.get("userId"):
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    if comment_update.content is not None:
        target_comment["content"] = comment_update.content

    comments[target_index] = target_comment
    save_data(COMMENTS_FILE, comments)

    return {"status": "success", "data": target_comment}

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, current_user: dict = Depends(get_current_user)):
    comments = load_data(COMMENTS_FILE)

    target_index = -1
    for i in range(len(comments)):
        if comments[i].get("id") == comment_id:
            target_index = i
            break

    if target_index == -1:
        raise HTTPException(status_code=404, detail="댓글이 없습니다.")

    if comments[target_index].get("writerId") != current_user.get("userId"):
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    comments.pop(target_index)
    save_data(COMMENTS_FILE, comments)

    return {"status": "success", "message": "삭제 완료"}

@app.get("/users/me/comments")
def get_user_comments(current_user: dict = Depends(get_current_user)):
    comments = load_data(COMMENTS_FILE)

    my_comments = []
    for c in comments:
        if c.get("writerId") == current_user.get("userId"):
            my_comments.append(c)
    return my_comments

# 여기까지 Comments

# Likes
import json
import os
import sys
import threading
from datetime import datetime, timedelta, timezone
from json import JSONDecodeError
from typing import Optional
import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
import pymysql



def get_db():
    conn = pymysql.connect(

    host = os.getenv('DB_HOST'),
    port = int(os.getenv('DB_PORT')),
    password = os.getenv('DB_PASSWORD'),
    db = os.getenv('DB_NAME'),
    charset = 'utf8mb4'
    )

    try:
        yield conn

    finally:
        conn.close()


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    print("ERROR: 환경 변수가 설정되지 않았습니다.")
    print("인프라 보안을 위해 서버 실행을 중단합니다.")
    sys.exit(1)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
POSTS_FILE = os.path.join(DATA_DIR, "posts.json")
COMMENTS_FILE = os.path.join(DATA_DIR, "comments.json")
LIKES_FILE = os.path.join(DATA_DIR, "likes.json")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

app = FastAPI()
security = HTTPBearer()

user_lock = threading.Lock()
post_lock = threading.Lock()
comment_lock = threading.Lock()
like_lock = threading.Lock()

DUMMY_PASSWORD = "dummy_password"
DUMMY_HASH = bcrypt.hashpw(DUMMY_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


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


def load_data(filename, default=None):
    if default is None:
        default = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        return default


def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
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

@app.post("/users/signup", status_code=201)
def signup(user: User):
    with user_lock:
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
        saved_pw_hash = target_user.get("password", "")
    else:
        saved_pw_hash = DUMMY_HASH

    is_pw_correct = bcrypt.checkpw(user.password.encode("utf-8"), saved_pw_hash.encode("utf-8"))

    if target_user is not None and is_pw_correct:
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
    with user_lock:
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
    user_id = current_user.get("userId")
    email = current_user.get("email")

    with user_lock:
        users = load_data(USERS_FILE)
        new_users = [u for u in users if u.get("email") != email]
        if len(users) == len(new_users):
            return {"msg": "탈퇴에 실패하였습니다."}
        save_data(USERS_FILE, new_users)

    with post_lock:
        posts = load_data(POSTS_FILE)
        new_posts = [p for p in posts if p.get("writerId") != user_id]
        save_data(POSTS_FILE, new_posts)

    with comment_lock:
        comments = load_data(COMMENTS_FILE)
        new_comments = [c for c in comments if c.get("writerId") != user_id]
        save_data(COMMENTS_FILE, new_comments)

    with like_lock:
        likes = load_data(LIKES_FILE)
        new_likes = [l for l in likes if l.get("userId") != user_id]
        save_data(LIKES_FILE, new_likes)

    return {"status": "success", "message": "회원 탈퇴 완료"}


@app.get("/users/me/posts")
def get_my_posts(current_user: dict = Depends(get_current_user)):
    posts = load_data(POSTS_FILE)
    my_posts = [p for p in posts if p.get("writerId") == current_user.get("userId")]
    my_posts.sort(key=lambda x: x.get("id", 0), reverse=True)
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

@app.post("/posts")
def create_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    with post_lock:
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
    sort_index = []
    if keyword is None:
        sort_index = posts
    else:
        for p in posts:
            if (keyword in p.get("title", "")) or (keyword in p.get("content", "")):
                sort_index.append(p)

    if sort == "views":
        sort_index.sort(key=lambda x: x.get("views", 0), reverse=True)
    else:
        sort_index.sort(key=lambda x: x.get("id", 0), reverse=True)

    limit = 5
    current_page = max(1, page)
    start_index = (current_page - 1) * limit
    end_index = start_index + limit
    result_posts = sort_index[start_index:end_index]
    return {"total": len(sort_index), "page": current_page, "data": result_posts}


@app.get("/posts/{post_id}")
def get_post_detail(post_id: int):
    with post_lock:
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
def patch_post_detail(post_id: int, post_update: PostUpdate, current_user: dict = Depends(get_current_user)):
    with post_lock:
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
    with post_lock:
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


@app.get("/posts/{post_id}/comments")
def get_comments(post_id: int):
    comments = load_data(COMMENTS_FILE)
    post_comments = [c for c in comments if c.get("postId") == post_id]
    return {"count": len(post_comments), "data": post_comments}


def post_exists(post_id):
    posts = load_data(POSTS_FILE)
    for p in posts:
        if p.get("id") == post_id:
            return
    raise HTTPException(status_code=404, detail="게시글이 없습니다.")


@app.post("/posts/{post_id}/comments")
def create_comment(post_id: int, comment: CommentCreate, current_user: dict = Depends(get_current_user)):
    post_exists(post_id)
    with comment_lock:
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
def update_comment(comment_id: int, comment_update: CommentUpdate, current_user: dict = Depends(get_current_user)):
    with comment_lock:
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
    with comment_lock:
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
    my_comments = [c for c in comments if c.get("writerId") == current_user.get("userId")]
    return my_comments

@app.post("/posts/{post_id}/likes")
def add_like(post_id: int, current_user: dict = Depends(get_current_user)):
    post_exists(post_id)
    with like_lock:
        likes = load_data(LIKES_FILE)
        for like in likes:
            if like.get("userId") == current_user.get("userId") and like.get("postId") == post_id:
                raise HTTPException(status_code=409, detail="이미 좋아요를 눌렀습니다.")
        new_like = {
            "userId": current_user.get("userId"),
            "postId": post_id,
            "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        likes.append(new_like)
        save_data(LIKES_FILE, likes)

    with post_lock:
        posts = load_data(POSTS_FILE)
        for p in posts:
            if p.get("id") == post_id:
                p["likes"] = p.get("likes", 0) + 1
                break
        save_data(POSTS_FILE, posts)
    return {"status": "success", "message": "좋아요 등록 완료"}


@app.delete("/posts/{post_id}/likes")
def remove_like(post_id: int, current_user: dict = Depends(get_current_user)):
    post_exists(post_id)
    with like_lock:
        likes = load_data(LIKES_FILE)
        target_index = -1
        for i, like in enumerate(likes):
            if like.get("userId") == current_user.get("userId") and like.get("postId") == post_id:
                target_index = i
                break
        if target_index == -1:
            raise HTTPException(status_code=404, detail="좋아요를 누르지 않았습니다.")
        likes.pop(target_index)
        save_data(LIKES_FILE, likes)

    with post_lock:
        posts = load_data(POSTS_FILE)
        for p in posts:
            if p.get("id") == post_id:
                current_likes = p.get("likes", 0)
                if current_likes > 0:
                    p["likes"] = current_likes - 1
                break
        save_data(POSTS_FILE, posts)
    return {"status": "success", "message": "좋아요 취소 완료"}


@app.get("/posts/{post_id}/likes")
def get_like_status(post_id: int, current_user: dict = Depends(get_current_user)):
    likes = load_data(LIKES_FILE)
    posts = load_data(POSTS_FILE)
    is_liked = False
    for like in likes:
        if like.get("userId") == current_user.get("userId") and like.get("postId") == post_id:
            is_liked = True
            break
    total_likes = 0
    for p in posts:
        if p.get("id") == post_id:
            total_likes = p.get("likes", 0)
            break
    return {"postId": post_id, "isLiked": is_liked, "totalLikes": total_likes}


@app.get("/users/me/likes")
def get_my_liked_posts(current_user: dict = Depends(get_current_user)):
    likes = load_data(LIKES_FILE)
    posts = load_data(POSTS_FILE)
    my_liked_post_ids = set()
    for like in likes:
        if like.get("userId") == current_user.get("userId"):
            my_liked_post_ids.add(like.get("postId"))
    liked_posts = []
    for p in posts:
        if p.get("id") in my_liked_post_ids:
            liked_posts.append(p)
    liked_posts.sort(key=lambda x: x.get("id", 0), reverse=True)
    return {"count": len(liked_posts), "data": liked_posts}
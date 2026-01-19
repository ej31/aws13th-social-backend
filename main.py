# FastAPI 앱 진입점
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from routers import auth, users, posts, comments, likes

app = FastAPI(title="클라우드 커뮤니티 API")

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)

@app.get("/")
async def root():
    return {"message": "Cloud Community API"}
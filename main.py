# FastAPI 앱 진입점
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from routers import auth, users, posts, comments, likes
from database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행되는 이벤트"""
    # 시작 시
    print("데이터베이스 연결 중...")
    try:
        await init_db()
        print("데이터베이스 연결 성공!")
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")
        raise

    yield

    # 종료 시
    print("데이터베이스 연결 종료 중...")
    await close_db()
    print("데이터베이스 연결 종료 완료!")


app = FastAPI(
    title="클라우드 커뮤니티 API",
    lifespan=lifespan
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)

@app.get("/")
async def root():
    return {"message": "Cloud Community API"}